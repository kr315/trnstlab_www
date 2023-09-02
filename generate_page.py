# =================================================
#       PAGE GENERATION
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

import random
import os
os.chdir(os.path.dirname(__file__))


def create_page():
    snippets = ['snippets/head.html',
                'snippets/menu.html',
                'snippets/foot.html'
    ]
    filename = 'index.html'
    
    # snippet buffering
    for idx, snippet_path in enumerate(snippets):
        with open(snippet_path, 'r') as f:
            snippets[idx] = f.read()

    # writing to file
    output_file_handle = open(filename, 'w')
    output_file_handle.write(snippets[0])               # head
    output_file_handle.write(create_index_content())
    output_file_handle.write(snippets[2])               # foot
    output_file_handle.close()

    # report
    print('written:\t' + filename)

def create_index_content():
    index_content_file = 'snippets/index_content.html'
    index_content = '\n'
    index_content += open(index_content_file, 'r').read() + '\n\n'
    # index_content += generate_blinds(columns=7, length=30, width=3, size_in_px=568)
    return index_content

def create_pictures_content():
    portfolio_directory = 'pictures-content'
    portfolio_content = ''
    png_list = []
    txt_list = []
    for filename in os.listdir(portfolio_directory):
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

        portfolio_content += '<div id=\'pictures-container\'><div id=\'floated\'>' + \
            '<img src=\'' + portfolio_directory + '\\' + element + '.png\' loading=\'lazy\'' + \
            '></div>' + element[0:4] + '<br>' + element_txt + '</div>'

    # print(content_list) 
    return portfolio_content

def create_menu():
    menu = '' 
    # mdfiles tree
    return menu

def create_bio():
    html_code = ''
    with open('snippets/head.html', 'r') as file_handle:
        html_code += file_handle.read()
    with open('portfolio/art-bio.md', 'r') as file_handle:
        bio_file = file_handle.readlines()
        html_code += '<h1>Biogram</h1>\n'
        for idx ,line in enumerate(bio_file):
            if '##' in line:
                html_code += '<h2>' + line.replace('## ', '').replace('\n', '') + '</h2>\n<ul>\n'
                print(idx)
                for jdx ,element in enumerate(bio_file[idx+1:]):
                    if line.startswith('!'):
                        pass
                    elif element.startswith('-'):
                        splitline = element.replace('- ', '').replace('\n', '').split(' / ')
                        html_code += '<li><span>'
                        for i in splitline:
                            if i.startswith('http'):
                                html_code += '<a href=\"' + i + '\">' + i + '</a><br>\n'
                            else:
                                html_code += i + '<br>\n'
                        html_code += '</span></li>\n<br>'
                    elif element.startswith('\n'):
                        break
                html_code += '</ul>\n<br>\n'
        print(html_code)
        output_file = open('portfolio/index.html', 'w+')
        output_file.writelines(html_code)
        output_file.close()

def create_visual():
    html_code = ''
    files = []
    with open('snippets/head.html', 'r') as file_handle:
        html_code += file_handle.read()
    for filename in os.listdir('visual'):
        files.append(filename)
    random.shuffle(files)
    for filename in files:
        if filename.endswith('mp4'):
            html_code += '<video autoplay loop muted><source src=\"' + filename + '\" type="video/mp4"></video>\n'
        elif filename.endswith('jpg'):
            html_code += '<img src=\"' + filename + '\">\n'    
    output_file = open('visual/index.html', 'w+')
    output_file.writelines(html_code)
    output_file.close()

    

# =============  EFFECTS  ======================

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

# create_bio()
create_visual()
