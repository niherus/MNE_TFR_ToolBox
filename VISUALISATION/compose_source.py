import os
import pdfkit

def clear_html(filename):
    with open(filename, 'w') as f:
        f.write('')

def add_str_html(filename, text):
    with open(filename, 'a') as f:
        f.write(text + '\n')

def add_pic_line_html(filename, pic_folder, pic_list):
    width = 210
    add_str_html(filename, "<p>")
    for pic in pic_list:
        add_str_html(filename, f'<img src="../{pic_folder}/{pic}" width="{width}">')
    add_str_html(filename, "</p>")

config = pdfkit.configuration(wkhtmltopdf='D:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

options = {
    'page-size':'A4',
    'orientation':'Portrait',
    'no-outline':None,
    'quiet':''
}

html_folder = "D:\\beta_data\\stc_look\\html_doc\\"
folders = ["p-val_w1_w2", "p-val_w1_w2-end", "p-val_d1_d2", "p-val_d1_d2-end"]
views = ['lat','med', 'med','lat']
hemies = ["lh", "lh", "rh", "rh"]
combines = list(zip(hemies, views))

for folder in folders:
    print(folder)
    html_name = os.path.join(html_folder, folder + ".html")
    clear_html(html_name)
    add_str_html(html_name, '<!DOCTYPE html>')
    add_str_html(html_name, '<html>')
    add_str_html(html_name, '<body>')
    for ind in range(20, 121):
        pic_list = []
        for combine in combines:
            num = "%04d"%(ind)
            pic_list.append(f"{combine[0]}_{combine[1]}_{num}.png")
        add_pic_line_html(html_name, folder, pic_list)
    add_str_html(html_name, '</body>')
    add_str_html(html_name, '</html>')
    pdfkit.from_file(html_name, html_name[:-4] + "pdf", configuration = config, options=options)


