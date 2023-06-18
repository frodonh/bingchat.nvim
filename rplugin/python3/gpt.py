import pynvim
import asyncio
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle


@pynvim.plugin
class Gpt(object):
    def __init__(self, vim):
        self.vim = vim
        self.bot = None
        self.conversation_style = ConversationStyle.balanced
        self.bufnr = None
        self.register = 'g'
        opts = self.vim.exec_lua("vim.g._bingchat_setup_options = require'bingchat-nvim'._setup_options")
        opts = self.vim.eval('g:_bingchat_setup_options')
        if not isinstance(opts, dict):
            opts = dict()
        update_keys = ['register', 'conversation_style']
        for k in update_keys:
            if k in opts:
                setattr(self, k, opts[k])

    def __del__(self):
        if self.bot is not None:
            asyncio.ensure_future(self.bot.close())

    def set_conversation_style(self, val):
        if val == 'creative':
            self.conversation_style = ConversationStyle.creative
        elif val == 'precise':
            self.conversation_style = ConversationStyle.precise
        else:
            self.conversation_style = ConversationStyle.balanced

    @pynvim.function('SetupGpt')
    def setupGpt(self, args):
        if 'register' in args[0]:
            self.register = args[0]['register']
        if 'conversation_style' in args[0]:
            self.set_conversation_style(args[0]['conversation_style'])

    @pynvim.command('SetGptStyle', nargs=1)
    def setgptstyle(self, args):
        self.set_conversation_style(args[0])

    async def async_send_to_gpt(self, text, buffer, lineno, allowmod=True):
        if self.bot is None:
            self.bot = await Chatbot.create()
        try:
            answer = await self.bot.ask(prompt=text, conversation_style=self.conversation_style)
            if 'item' in answer and 'messages' in answer['item']:
                l = len(answer['item']['messages'])-1
                while l >= 1 and answer['item']['messages'][l]['adaptiveCards'][0]['body'][0]['type'] != 'TextBlock':
                    l = l-1
                if l >= 1:
                    if buffer is not None:
                        self.vim.async_call(buffer.append, answer["item"]["messages"][l]["adaptiveCards"][0]["body"][0]["text"].splitlines(), lineno)
                        if not allowmod and self.bufnr is not None:
                            self.vim.async_call(self.vim.exec_lua, 'vim.bo[' + str(self.bufnr) + '].modifiable=false')
                    else:
                        self.vim.funcs.setreg(self.register , answer["item"]["messages"][l]["adaptiveCards"][0]["body"][0]["text"], 'c', async_=True)
                        self.vim.out_write("Answer loaded in register '" + self.register + "'\n", async_=True)
        except Exception as error:
            self.vim.err_write('Gpt exception: ', type(error).__name__, ' - ', error, "\n")

    @pynvim.command('GptToBuf', nargs='?', range='', bang=True)
    def gpttobuf(self, args, range, bang):
        buf = self.vim.current.buffer
        line = self.vim.current.window.cursor[0]
        prompt = ""
        if len(args) > 0:
            prompt = args[0] + "\n"
        if not bang:
            lines = self.vim.current.buffer[range[0]-1:range[1]]
            prompt = prompt + "\n".join(lines)
        # self.vim.out_write(prompt+"\n")
        asyncio.ensure_future(self.async_send_to_gpt(prompt, buf, line))

    @pynvim.command('GptToReg', nargs='?', range='', bang=True)
    def gpttoreg(self, args, range, bang):
        prompt = ""
        if len(args) > 0:
            prompt = args[0] + "\n"
        if not bang:
            lines = self.vim.current.buffer[range[0]-1:range[1]]
            prompt = prompt + "\n".join(lines)
        asyncio.ensure_future(self.async_send_to_gpt(prompt, None, -1))

    @pynvim.command('GptToScratch', nargs='?', range='', bang=True)
    def gpttoscratch(self, args, range, bang):
        prompt = ""
        if len(args) > 0:
            prompt = args[0] + "\n"
        if not bang:
            lines = self.vim.current.buffer[range[0]-1:range[1]]
            prompt = prompt + "\n".join(lines)
        self.bufnr = self.vim.exec_lua('return vim.api.nvim_create_buf(false,true)')
        self.winid = self.vim.exec_lua('return vim.api.nvim_open_win(' + str(self.bufnr) + ',true,{title="GPT",title_pos="center",relative="editor",row=math.floor(((vim.o.lines - 20) / 2) - 1),col=math.floor(vim.o.columns/2-30),height=20,width=60,style="minimal",border="rounded"})')
        self.vim.exec_lua('vim.api.nvim_win_set_option(' + str(self.winid) + ',"winblend", 0)')
        self.vim.exec_lua('vim.keymap.set({"n"},"<Esc>",function() vim.api.nvim_buf_delete(' + str(self.bufnr) + ',{force=true}) end,{buffer=' + str(self.bufnr) +',silent=true})')
        asyncio.ensure_future(self.async_send_to_gpt(prompt, self.vim.buffers[self.bufnr], -1, False))

    @pynvim.command('ResetGpt', nargs=0)
    def reset_gpt(self, args):
        async def create_bot(self):
            self.bot = await Chatbot.create()

        if self.bot is not None:
            asyncio.ensure_future(self.bot.close())
        asyncio.ensure_future(create_bot(self))
