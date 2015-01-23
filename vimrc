" An example for a vimrc file.
"
" Maintainer:	Bram Moolenaar <Bram@vim.org>
" Last change:	2008 Dec 17
"
" To use it, copy it to
"     for Unix and OS/2:  ~/.vimrc
"	      for Amiga:  s:.vimrc
"  for MS-DOS and Win32:  $VIM\_vimrc
"	    for OpenVMS:  sys$login:.vimrc

" When started as "evim", evim.vim will already have done these settings.
if v:progname =~? "evim"
  finish
endif

" Use Vim settings, rather than Vi settings (much better!).
" This must be first, because it changes other options as a side effect.
set nocompatible

" allow backspacing over everything in insert mode
set backspace=indent,eol,start

if has("vms")
  set nobackup		" do not keep a backup file, use versions instead
    set nowritebackup
else
  set backup		" keep a backup file
  set writebackup
  set backupdir=~/tmp

endif
set history=50		" keep 50 lines of command line history
set ruler		" show the cursor position all the time
set showcmd		" display incomplete commands
set incsearch		" do incremental searching

" For Win32 GUI: remove 't' flag from 'guioptions': no tearoff menu entries
" let &guioptions = substitute(&guioptions, "t", "", "g")

" Don't use Ex mode, use Q for formatting
map Q gq

" CTRL-U in insert mode deletes a lot.  Use CTRL-G u to first break undo,
" so that you can undo CTRL-U after inserting a line break.
inoremap <C-U> <C-G>u<C-U>

" In many terminal emulators the mouse works just fine, thus enable it.
if has('mouse')
  set mouse=v
endif

" Switch syntax highlighting on, when the terminal has colors
" Also switch on highlighting the last used search pattern.
if &t_Co > 2 || has("gui_running")
  syntax on
  set hlsearch
endif

" Only do this part when compiled with support for autocommands.
if has("autocmd")

  " Enable file type detection.
  " Use the default filetype settings, so that mail gets 'tw' set to 72,
  " 'cindent' is on in C files, etc.
  " Also load indent files, to automatically do language-dependent indenting.
  filetype plugin indent on

  " Put these in an autocmd group, so that we can delete them easily.
  augroup vimrcEx
  au!

  " For all text files set 'textwidth' to 78 characters.
  autocmd FileType text setlocal textwidth=78

  " When editing a file, always jump to the last known cursor position.
  " Don't do it when the position is invalid or when inside an event handler
  " (happens when dropping a file on gvim).
  " Also don't do it when the mark is in the first line, that is the default
  " position when opening a file.
  autocmd BufReadPost *
    \ if line("'\"") > 1 && line("'\"") <= line("$") |
    \   exe "normal! g`\"" |
    \ endif

  augroup END

else

set autoindent		" always set autoindenting on


endif " has("autocmd")

" Convenient command to see the difference between the current buffer and the
" file it was loaded from, thus the changes you made.
" Only define it when not defined already.
if !exists(":DiffOrig")
  command DiffOrig vert new | set bt=nofile | r # | 0d_ | diffthis
		  \ | wincmd p | diffthis
endif
			
set guifont=Courier_New:h16
set guifontwide=STXihei:h16

set nocompatible               " be iMproved
filetype off                   " required!

set rtp+=~/.vim/bundle/vundle/
call vundle#rc()

" let Vundle manage Vundle
" required! 
Bundle 'gmarik/vundle'

" My Bundles here:
"
" original repos on github
Bundle 'tpope/vim-fugitive'
Bundle 'Lokaltog/vim-easymotion'
Bundle 'rstacruz/sparkup', {'rtp': 'vim/'}
Bundle 'tpope/vim-rails.git'
" vim-scripts repos
Bundle 'L9'
Bundle 'FuzzyFinder'
Bundle 'SuperTab'
Bundle 'word_complete.vim'
Bundle 'python.vim'
Bundle 'Pydiction'
Bundle 'vim-markdown'
Bundle 'hammer.vim'
Bundle 'instant-markdown.vim'
" non github repos
Bundle 'git://git.wincent.com/command-t.git'
" git repos on your local machine (ie. when working on your own plugin)
Bundle 'file:///Users/gmarik/path/to/plugin'
" ...
Bundle 'snipMate'
Bundle 'pythoncomplete'


filetype plugin indent on     " required!
"
" Brief help
" :BundleList          - list configured bundles
" :BundleInstall(!)    - install(update) bundles
" :BundleSearch(!) foo - search(or refresh cachefirst) for foo
" :BundleClean(!)      - confirm(orauto-approve) removal of unused bundles
"
" see :h vundle for more details or wiki for FAQ
" NOTE: comments after Bundle command are not allowed..
"

"pydiction 1.2 python auto complete

" hammer  markdown
if has('unix')
           let g:HammerBrowser = 'w3m'
       end
       map <leader>p :Hammer<CR>
"hammer markdown

 filetype plugin on

 let g:pydiction_location = '~/.vim/tools/pydiction/complete-dict'
 

 "defalut g:pydiction_menu_height == 15

 "let g:pydiction_menu_height = 20 

set shiftwidth=4
set ts=4
set expandtab

"auto add pyhton header --start
autocmd BufNewFile *.py 0r ~/.vim/template/py.clp
autocmd BufNewFile *.py ks|call FileName()|'s
autocmd BufNewFile *.py ks|call CreatedTime()|'s

fun FileName()
    if line("$") > 10
        let l = 10  "这里是字母L 不是数字1 
    else
        let l = line("$")
    endif 
    exe "1," . l . "g/File Name:.*/s/FileName:.*/File Name: " .expand("%")  
    "最前面是数字1，这里的File Name:要和模板中一致
endfun 

fun CreatedTime()
    if line("$") > 10
        let l = 10
    else
        let l = line("$")
    endif 
    exe "1," . l . "g/Created Time:.*/s/Created Time:.*/Created Time: ".strftime("%Y-%m-%d %T") 
    "这里Create Time:要和模板中一致
endfun 
"auto add python header --end
"
"auto add bash header --start

autocmd BufNewFile *.sh 0r ~/.vim/template/sh
autocmd BufNewFile *.sh ks|call CreatedTime()|'s

"auto add bash header --end
