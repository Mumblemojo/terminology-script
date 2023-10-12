import pyperclip
import PySimpleGUI as gui
from pathlib import Path
import json
import os
import webbrowser

layout = [[gui.Text("Hallo, Jojo")], [gui.Button("fr_context"),
                                      gui.Button("fr_pons"),
                                      gui.Button("fr_commas"), 
                                      gui.Button("fr_file"),
                                      gui.Button("fr_cleanup"),],
                                     [gui.Button("it_context"),
                                      gui.Button("it_pons"),
                                      gui.Button("it_trec"),
                                      gui.Button("it_wiki"),
                                      gui.Button("it_file"),
                                      gui.Button("it_cleanup",)],
                                     [gui.Button("en_context"),
                                      gui.Button("en_dict"),
                                      gui.Button ("en_wiki"),
                                      gui.Button("en_file"),
                                      gui.Button("en_cleanup"),]]
window = gui.Window("Terminologie", layout, margins=(100, 100))

class Language():
    '''represents a language, with path to the textfile it works with
    and the links to several dictionaries. can take terms from clipboard
    and, generate links in each dict, and open those links in browser tabs'''
    def __init__(self, path, dict_a, dict_b = None, dict_c = None, 
                 dict_d = None):
        self.path = path
        self.dict_a = dict_a
        self.dict_b = dict_b
        self.dict_c = dict_c
        self.dict_d = dict_d


    def cleanup_file(self):
        '''rearrange file, so that unfinished terminology is on top (needs to 
        have ';' at the end), finished terminology on bottom with two blank 
        lines as seperator, and sentences ending with '**' are written to
         the file 'sentences.txt '''
        path = Path(self.path)
        path_2 = Path('C:/Users/Joachim/Desktop/sentences.txt')
        content = path.read_text(encoding= 'UTF-8').strip()
        contents=content.splitlines()
        print(contents)
        contents = [i for i in contents if i]
        print(contents)
        completed = []
        remains = []
        sentences = []
        while contents:
            line = contents.pop().strip()
            if line.endswith(';') == True or ';' not in line:
                remains.append(line)
            elif line.endswith('**') == True:
                sentences.append(line)
            else:
                completed.append(line)
        output_1 = ""
        for line in remains:
            line = line.removesuffix(';')
            output_1 += line + '\n'
        output_2 = ""
        for line in completed:
            output_2 += line + '\n'
        new_file = f"{output_1}\n\n{output_2}"
        path.write_text(new_file, encoding='UTF-8')
        os.startfile(path)
        output_3 = ''
        for sentence in sentences:
            sentence = sentence.removesuffix('**')
            output_3 += sentence + '\n'
        path_2.write_text(output_3, encoding ='UTF-8')
        

    def make_clipboard_links(self, dict_x):
        '''take text from clipboard as string. split into lines. Add ";" to each
        line (for anki formatting) and write to specified textfile (path).
        combine each line with dictionary link (text_a), and open all links as 
        browser tabs. open textfile.
        '''
        dict_x = dict_x
        startpath = self.path
        path = Path(self.path)
        clipboard_text = pyperclip.paste().strip()
        old_text = "\n\n" + path.read_text(encoding = "UTF-8") 
        lines = clipboard_text.split('\n')
        output = ""
        for line in lines:
            line = line.removesuffix('\r')
            line += ';'
            output += line + "\n"
        output += old_text
        path.write_text(output, encoding="UTF-8")
        os.startfile(startpath)
        output = ""
        for line in lines:
            combined = dict_x + line
            webbrowser.open_new_tab(combined)


    def copy_from_file(self):
        '''delete all occurrences of ";" in specified file, copy contents
        to clipboard, overwrites text in file with blank string'''
        path = Path(self.path)
        text = path.read_text(encoding='UTF-8')
        empty = ''
        path.write_text(empty, encoding = 'UTF-8')
        text = text.replace(';', '')
        print(text)
        pyperclip.copy(text)
    
    
    def commas(self):
        '''takes terms separated by commas from clipboard,
           makes them separated by line (in clipboard).
        '''
        raw = pyperclip.paste().strip()
        new = raw.split(',')
        output = ""
        for line in new:
            output += line.strip() +"\n"
        pyperclip.copy(output)
       

french = Language('C:/Users/Joachim/Desktop/francais.txt', 
                  "https://context.reverso.net/translation/french-german/", 
                  "https://en.pons.com/translate/french-german/",
                  )
italian = Language('C:/Users/Joachim/Desktop/italiano.txt',
                   'https://context.reverso.net/translation/italian-german/',
                   'https://de.pons.com/%C3%BCbersetzung/italienisch-deutsch/',
                   'https://www.treccani.it/vocabolario/',
                   'https://it.wikipedia.org/wiki/',
                   )
english = Language('C:/Users/Joachim/Desktop/english.txt',
                   "https://context.reverso.net/translation/english-german/",
                   "https://www.dict.cc/?s=",
                   'https://en.wikipedia.org/wiki/',
                   )

while True:
    event, values = window.read()
    if event == gui.WIN_CLOSED:
        break
    if event == "fr_context":
        french.make_clipboard_links(french.dict_a)
    if event == "fr_pons":
        french.make_clipboard_links(french.dict_b)
    if event == "fr_cleanup":
        french.cleanup_file()
    if event == "fr_file":
        french.copy_from_file()
    if event == 'fr_commas':
        french.commas()
    if event == "it_context":
        italian.make_clipboard_links(italian.dict_a)   
    if event == "it_pons":
        italian.make_clipboard_links(italian.dict_b)
    if event == "it_trec":
        italian.make_clipboard_links(italian.dict_c)
    if event == 'it_wiki':
        italian.make_clipboard_links(italian.dict_d)
    if event == "it_file":
        italian.copy_from_file()
    if event == "it_cleanup":
        italian.cleanup_file()
    if event == "en_context":
        english.make_clipboard_links(english.dict_a)
    if event == "en_dict":
        english.make_clipboard_links(english.dict_b)
    if event == 'en_wiki':
        english.make_clipboard_links(english.dict_c)
    if event == "en_file":
        english.copy_from_file()
    if event == "en_cleanup":
        english.cleanup_file()

    

    
