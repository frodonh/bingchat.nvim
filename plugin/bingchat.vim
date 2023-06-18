" Title:        BingChat plugin
" Description:  A plugin to chat with GPT from inside Neovim
" Last Change:  June 17th, 2023
" Maintainer:   François Hissel

" Prevents the plugin from being loaded multiple times. If the loaded
" variable exists, do nothing more. Otherwise, assign the loaded
" variable and continue running this instance of the plugin.
if exists("g:loaded_bingchatplugin")
    finish
endif
let g:loaded_bingchatplugin = 1
