import os
import glob
from html.parser import HTMLParser

VOID_TAGS = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr', '!doctype'}

class Validator(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.stack = []
        self.errors = []
        
    def handle_starttag(self, tag, attrs):
        if tag not in VOID_TAGS:
            self.stack.append((tag, self.getpos()))
            
    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        
        # Pop until we find the matching tag
        found = False
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                # Found it. Pop all unclosed tags after it
                unclosed = self.stack[i+1:]
                for un_tag, pos in unclosed:
                    self.errors.append(f"Unclosed tag <{un_tag}> at line {pos[0]} col {pos[1]}")
                self.stack = self.stack[:i] # pop it and everything after
                found = True
                break
        if not found:
            self.errors.append(f"Unexpected closing tag </{tag}> at line {self.getpos()[0]} col {self.getpos()[1]}")

    def get_errors(self):
        for un_tag, pos in self.stack:
            self.errors.append(f"Unclosed tag <{un_tag}> at line {pos[0]} col {pos[1]}")
        return self.errors

def main():
    files = glob.glob('**/*.html', recursive=True)
    exclude = ['snapshot', 'staging', 'wp-content', '.wrangler']
    for f in files:
        if any(ex in f for ex in exclude):
            continue
        try:
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
            parser = Validator(f)
            parser.feed(content)
            errors = parser.get_errors()
            if errors:
                print(f"--- {f} ---")
                for e in errors:
                    print("  ", e)
        except Exception as e:
            print(f"Failed to parse {f}: {e}")

if __name__ == '__main__':
    main()
