import re
import os
import sys

def RemoveTag(line):
    line = re.sub(r'\#{1}[^#\s]+', "", line)
    return line

def ConvertFile(file):
    # 1. convert the admonition format
    # 2. remove the tag in the line
    with open(file, 'r') as f, open('.temp.md', 'w') as buffer:
        
        match_admonition = False
        footnote_id = 0
        footnote_list = []
        footnote_dict = {}

        for line in f:

            # begin of the admonition
            if re.search('```ad-info', line):
                match_admonition = True
                buffer.write('!!! info' + '\n')
                continue
            # end of the admonition
            elif re.search('\s*```\s*$', line) and match_admonition:
                match_admonition = False
                buffer.write('\n')
                continue
            
            line = RemoveTag(line)

            # extract the footntoe in the end
            if re.search('\[\^[^\]]*\]:', line):
                foot_element_end = re.search('\[\^[^\]]*\]:', line).group() # match "[^xxx]:"
                if foot_element_end is not None:
                # print(type(foot_element_end))
                    foot_element_end = foot_element_end[:-1] # [^xxx]: -> [^xxx]
                    print("match footnote:" + foot_element_end)

                    if footnote_list.count(foot_element_end) > 0:
                        foot_element_content = re.sub('\[\^[^\]]*\]:', "", line)
                        new_footnote = {foot_element_end: foot_element_content}
                        footnote_dict.update(new_footnote)
                        continue
                    else:
                        print("\033[31m[ERROR!]\033[0m[" + file + "]: " + "Existence of non-matching footnotes!", file=sys.stderr)        
                        return

            # extract the footnote in the text and push it into list in order
            if re.search('\[\^[^\]]*\]', line):
                foot_element = re.search('\[\^[^\]]*\]', line).group() # match "[^xxx]"
                if foot_element and footnote_list.count(foot_element) == 0:
                    print("find footnote:" + foot_element)
                    footnote_list.append(foot_element)

            # If in admonition, add tab before the line
            # Otherwise, output straightforwardly
            if match_admonition:
                buffer.write('\t' + line)
            else:
                buffer.write(line)
        
        for foot_element in footnote_list:
            buffer.write(foot_element + ":" + footnote_dict.get(foot_element))

        # close files and flush the buffer
        buffer.close()
        f.close()
        os.rename('.temp.md', file)
    return

def ImportFile(file):

    # only markdown file
    if re.search('\.md$', file) is None:
        return
    
    # convert file from obsidian form into mkdocs form
    ConvertFile(file)
    return