import re
import os

def ConvertFile(file):
    # 1. convert the admonition format
    with open(file, 'r') as f, open('.temp.md', 'w') as buffer:
        
        match_admonition = False
        for line in f:
            if re.search('```ad-info', line):
                match_admonition = True
                buffer.write('!!! info' + '\n')
                continue
            # end of the admonition
            elif re.search('\s*```\s*$', line) and match_admonition:
                match_admonition = False
                buffer.write('\n')
                continue
            
            if match_admonition:
                buffer.write('\t' + line)
            else:
                buffer.write(line)

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