from cgitb import html
from email import header
from os import listdir
import random

snippets = ['snippets/head.html',
            'snippets/menu.html',
            'snippets/foot.html'
]
index_content_file = 'snippets/index_content.html'
portfolio_directory = 'content' 

def main():

    create_page('index', snippets)
    # create_page('portfolio', snippets)
    print('\n---+>>> end')





# =================================================
#       BASIC PAGE GENERATION
#
#       HTML PAGE LAYOUT
#
#       +-----------+
#       | head.html |       snippets[0]
#       +-----------+
#       | menu.html |       snippets[1]
#       +-----------+
#       |  CONTENT  |
#       +-----------+
#       | foot.html |       snippets[2]
#       +-----------+
#
# page types:   index        - CONTENT generated from index_content.html snippet
#               portfolio    - CONTENT generated by putting together in a divs txt and png files 
#                               of the same names contained in 'portfolio_directory' 
#                               
#               ...          - new page
def create_page(page_type, snippets):
        filename, content = '', ''

        # page type selector, add new for new page type
        if page_type == 'index':
            content = create_index_content()
            filename = 'index.html'
        if page_type == 'portfolio':
            content = create_portfolio_content()
            filename = 'portfolio.html'
        
        # snippet buffering
        for idx, snippet_path in enumerate(snippets):
            with open(snippet_path, 'r') as f:
                snippets[idx] = f.read()

        # writing to file
        output_file_handle = open(filename, 'w')
        output_file_handle.write(snippets[0])               # head
        output_file_handle.write(snippets[1])               # menu

        output_file_handle.write(content)                   # content

        output_file_handle.write(snippets[2])               # foot
        output_file_handle.close()

        # report
        print('written:\t' + filename)

def create_index_content():
    index_content = '\n'
    index_content += open(index_content_file, 'r').read() + '\n\n'
    index_content += generate_blinds(columns=7, length=30, width=3, size_in_px=568)
    return index_content

def create_portfolio_content():
    portfolio_content = ''
    png_list = []
    txt_list = []
    for filename in listdir(portfolio_directory):
        if filename.endswith('.png'): png_list.append(filename[:-4])
        if filename.endswith('.txt'): txt_list.append(filename[:-4])
    for png in png_list:
        if png in txt_list:
            continue
        else:
            # raise exception
            print('\nerror: txt for png not found for ' + png + '\n\n')
            exit()

    txt_list.sort(reverse=True)
    for element in txt_list:
        element_txt = open(portfolio_directory + '/' + element + '.txt', 'r').read()

        portfolio_content += '<div id=\'container\'><div id=\'floated\'>' + \
            '<img src=\'' + portfolio_directory + '\\' + element + '.png\' loading=\'lazy\'' + \
            '></div>' + element[0:4] + '<br>' + element_txt + '</div>'

    # print(content_list) 
    return portfolio_content

# =================================================
#       EFFECTS
#
# generate blinds of random symbols in symbols_list
# 'columns' is number of columns fitted in size_in_px
# by columns of 'width' x 'length' symbols
def generate_blinds(columns, length, width, size_in_px):
    symbols_list = '!@#$^&*()_+|}{\'\':?>,./;[]\\=-'
    txt = ''
    w, l, c = width, length, columns
    while(c):
        txt += '<div class=\'blinds\' style=\'position: absolute; top: 0px; left: '
        txt += str((c-1)*size_in_px/(columns)) + 'px;\'>'
        l = length
        while(l):
            w = width
            while(w):
                txt += symbols_list[int(random.random()*len(symbols_list))]
                w -= 1
            txt += '<br>'
            l -= 1
        c -= 1
        txt += '</div>\n'
    return txt



main()