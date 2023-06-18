# BingChat.nvim

BingChat.nvim let you chat with Bing AI from inside Neovim.

## Features
BingChat plugin let you ask something to Bing AI without leaving NeoVim. The plugin is a remote-plugin written in Python. It adds a few new commands to your environment.

It does not create any new keymap. You have to configure them by yourself.

## Requirements

To use this plugin, you need Python3 and the [EdgeGpt](https://github.com/acheong08/EdgeGPT) module. You can install the module with the following command:

```bash
python3 -m pip install EdgeGPT --upgrade
```

The plugin needs a cookie to connect to Bing chat. You have to follow the instructions at <https://github.com/acheong08/EdgeGPT>:

- Open your browser and set the user-agent to something that looks like Microsoft Edge
- Open <https://bing.com/chat>
- If you see a chat feature, you are good to continue…
- Install the cookie editor extension for Chrome or Firefox
- Go to <https://bing.com>
- Open the extension
- Click "Export" on the bottom right, then "Export as JSON". This saves your cookies to clipboard
- Paste your cookies into a file `bing_cookies_*.json`
- Save the cookies file at the root of your home directory

If you comply with the previous requirements and the commands are not available when you open NeoVim, try to run the following command:

```vim
  :UpdateRemotePlugins
```

then restart NeoVim.

## Installation
Using [lazy.nvim](https://github.com/folke/lazy.nvim)
```lua
-- init.lua:
	{
		'frodonh/bingchat.nvim',
		build = ':UpdateRemotePlugins',
		opts = {
			-- You may add options here, but the following are the default values
	    	register = 'g',
	    	conversation_style = 'balanced'
		}
	}
```

## Customization

### Keymaps
This plugin does not create any keymap. You can add you own keymaps by configuring them in your `init.lua` file:
```lua
-- init.lua:
vim.keymap.set({'n','i'},'<F8>','<cmd>GptToReg<CR>',{silent=true,buffer=true,desc='Send current line to Bing AI'})
vim.keymap.set({'v'},'<F8>',':GptToReg<CR>',{silent=true,buffer=true,desc='Send current visual selection to Bing AI'})
```
### Configuration options
The configuration options can be set when the plugin is loaded (see [Installation](#Installation)), or using:

```lua
require 'Bingchat'.setup({
	register = 'h',
	conversation_style = 'creative'
})
```

| Option             | Default value |      Description                                                   |
|--------------------|---------------|--------------------------------------------------------------------|
| register           | 'g'           | A single character which identifies the register where the answer of a Bing AI request shall be loaded when :GptToReg[!] command is used |
| conversation_style | 'balanced'    | A string value defining the style of the Bing AI conversation. Three values are allowed : 'balanced', 'creative', 'precise' |

## Commands
The following commands are available when the plugin is installed.

| Command                  |  Description                                                                     |
|--------------------------|----------------------------------------------------------------------------------|
| `:\[range\]GptToBuf \[prompt\]` | Ask a question to Bing chat and append answer after cursor position in the current buffer. If specified, \[prompt\] is sent to Bing chat. If \[range\] is given, the prompt is followed by a newline and all the lines in the range. If no \[range\] is specified, the current line is used. |
| `:GptToBuf! {prompt}` | Ask a question to Bing chat and append answer after cursor position in the current buffer. {prompt} is sent to Bing chat. |
| `:\[range\]GptToReg \[prompt\]` | Ask a question to Bing chat and fill a register with the answer. If specified, \[prompt\] is sent to Bing chat. If \[range\] is given, the prompt is followed by a newline and all the lines in the range. If no \[range\] is specified, the current line is used. |
| `:GptToReg! \[prompt\]` | Ask a question to Bing chat and fill a register with the answer. If specified, \[prompt\] is sent to Bing chat. If \[range\] is given, the prompt is followed by a newline and all the lines in the range. If no \[range\] is specified, the current line is used. |
| `:GptToBuf! {prompt}` | Ask a question to Bing chat and append answer after cursor position in the current buffer. {prompt} is sent to Bing chat. |
| `:\[range\]GptToScratch \[prompt\]` | Ask a question to Bing chat and display the answer in a temporary floating window. The floating window may be closed by pressing `Esc`. If specified, \[prompt\] is sent to Bing chat. If \[range\] is given, the prompt is followed by a newline and all the lines in the range. If no \[range\] is specified, the current line is used. |
| `:GptToScratch! {prompt}` | Ask a question to Bing chat and display the answer in a temporary floating window. The floating window may be closed by pressing `Esc`. {prompt} is sent to Bing chat. |
| `:ResetGpt`  | Start a new conversation with Bing AI. All the previous dialogue is forgotten. |
| `:SetGptStyle {style}`  | Set the AI conversation style. Three values are allowed: 'balanced' (the default), 'precise' or 'creative' |

## Related plugins
- [nvim-gpt](https://github.com/archibate/nvim-gpt) also let you have a conversation with Bing Chat from inside Neovim. In addition, you can also use ChatGpt and Google Search from the same interface. It is really a good plugin but was a bit too opinionated and developers-oriented for me.
- [ChatGPT.nvim](https://github.com/jackMort/ChatGPT.nvim) is a vim-plugin for the OpenAI ChatGPT API. It provides a lot of features and a great customability, but to use it, you have to have an OpenAI token.
