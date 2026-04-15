import sys
import struct
import re
import argparse

# --- C64 BASIC V2 Token Map ---
TOKENS = {
    'END': 0x80, 'FOR': 0x81, 'NEXT': 0x82, 'DATA': 0x83, 'INPUT#': 0x84,
    'INPUT': 0x85, 'DIM': 0x86, 'READ': 0x87, 'LET': 0x88, 'GOTO': 0x89,
    'RUN': 0x8A, 'IF': 0x8B, 'RESTORE': 0x8C, 'GOSUB': 0x8D, 'RETURN': 0x8E,
    'REM': 0x8F, 'STOP': 0x90, 'ON': 0x91, 'WAIT': 0x92, 'LOAD': 0x93,
    'SAVE': 0x94, 'VERIFY': 0x95, 'DEF': 0x96, 'POKE': 0x97, 'PRINT#': 0x98,
    'PRINT': 0x99, 'CONT': 0x9A, 'LIST': 0x9B, 'CLR': 0x9C, 'CMD': 0x9D,
    'SYS': 0x9E, 'OPEN': 0x9F, 'CLOSE': 0xA0, 'GET': 0xA1, 'NEW': 0xA2,
    'TAB(': 0xA3, 'TO': 0xA4, 'FN': 0xA5, 'SPC(': 0xA6, 'THEN': 0xA7,
    'NOT': 0xA8, 'STEP': 0xA9, '+': 0xAA, '-': 0xAB, '*': 0xAC, '/': 0xAD,
    '^': 0xAE, 'AND': 0xAF, 'OR': 0xB0, '>': 0xB1, '=': 0xB2, '<': 0xB3,
    'SGN': 0xB4, 'INT': 0xB5, 'ABS': 0xB6, 'USR': 0xB7, 'FRE': 0xB8,
    'POS': 0xB9, 'SQR': 0xBA, 'RND': 0xBB, 'LOG': 0xBC, 'EXP': 0xBD,
    'COS': 0xBE, 'SIN': 0xBF, 'TAN': 0xC0, 'ATN': 0xC1, 'PEEK': 0xC2,
    'LEN': 0xC3, 'STR$': 0xC4, 'VAL': 0xC5, 'ASC': 0xC6, 'CHR$': 0xC7,
    'LEFT$': 0xC8, 'RIGHT$': 0xC9, 'MID$': 0xCA, 'GO': 0xCB,
}

# --- C64 Control Codes Map ---
# Usage: {CLR}, {WHT}, {DOWN}, etc. inside your strings.
CONTROLS = {
    # Colors
    'BLK': 144, 'WHT': 5,   'RED': 28,  'CYN': 159,
    'PUR': 156, 'GRN': 30,  'BLU': 31,  'YEL': 158,
    'ORNG': 129,'BRN': 149, 'LRED': 150,'GREY1': 151,
    'GREY2': 152,'LGRN': 153,'LBLU': 154,'GREY3': 155,
    
    # Cursor / Screen
    'CLR': 147, 'HOME': 19,
    'UP': 145,  'DOWN': 17, 'LEFT': 157, 'RIGHT': 29,
    'INST': 148,'DEL': 20,
    
    # Text Modes
    'RVS': 18,  'OFF': 146, # Reverse on/off
}

TOKEN_REPLACEMENTS = sorted(TOKENS.keys(), key=len, reverse=True)

def petscii_encode(char):
    """
    Standard ASCII to PETSCII mapping.
    Maps a-z to A-Z (standard C64 mode).
    """
    if 'a' <= char <= 'z':
        return ord(char.upper())
    return ord(char)

def replace_control_codes(text):
    """
    Replaces {TAG} patterns with their single-byte integer values.
    Returns a string where control chars are embedded as unicode code points.
    """
    def replace_match(match):
        tag = match.group(1).upper()
        if tag in CONTROLS:
            return chr(CONTROLS[tag])
        return match.group(0) # Return original if tag not found

    # Regex to find {TAG}
    return re.sub(r'\{([A-Za-z0-9]+)\}', replace_match, text)

def tokenize_line(line_text):
    """
    Converts a line of text into a byte array of tokens and PETSCII characters.
    Handles quoted strings (which should NOT be tokenized).
    """
    # 1. Expand {TAGS} before tokenizing
    line_text = replace_control_codes(line_text)
    
    output = bytearray()
    i = 0
    length = len(line_text)
    in_quote = False

    while i < length:
        char = line_text[i]
        
        # Toggle quote mode
        if char == '"':
            in_quote = not in_quote
            output.append(petscii_encode(char))
            i += 1
            continue

        # If inside quotes, output raw chars (including our control codes)
        if in_quote:
            output.append(petscii_encode(char))
            i += 1
            continue

        # Check for '?' shorthand for PRINT
        if char == '?':
            output.append(TOKENS['PRINT'])
            i += 1
            continue

        # Try to match a BASIC Keyword
        match_found = False
        current_slice = line_text[i:]
        
        for kw in TOKEN_REPLACEMENTS:
            if current_slice.startswith(kw):
                output.append(TOKENS[kw])
                i += len(kw)
                match_found = True
                break
        
        if not match_found:
            output.append(petscii_encode(char))
            i += 1

    output.append(0x00) # Null terminator for the line
    return output

def convert_to_prg(input_file, output_file):
    MEM_START = 0x0801 
    lines_data = []
    
    try:
        with open(input_file, 'r') as f:
            raw_lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}")
        sys.exit(1)

    # 1. Parse text lines
    for raw in raw_lines:
        raw = raw.strip()
        if not raw: continue 
        
        match = re.match(r'^(\d+)\s*(.*)', raw)
        if not match: continue
            
        line_num = int(match.group(1))
        code_text = match.group(2)
        
        tokenized_bytes = tokenize_line(code_text)
        lines_data.append((line_num, tokenized_bytes))

    lines_data.sort(key=lambda x: x[0])

    # 2. Build PRG
    prg_content = bytearray(struct.pack('<H', MEM_START))
    current_mem_address = MEM_START
    
    for line_num, code_bytes in lines_data:
        line_overhead = 4 
        next_address = current_mem_address + line_overhead + len(code_bytes)
        
        prg_content.extend(struct.pack('<H', next_address))
        prg_content.extend(struct.pack('<H', line_num))
        prg_content.extend(code_bytes)
        
        current_mem_address = next_address

    prg_content.extend(b'\x00\x00')

    with open(output_file, 'wb') as f:
        f.write(prg_content)
        
    print(f"Success! Converted {input_file} to {output_file}")
    print(f"Program size: {len(prg_content)} bytes.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 txt2prg_v2.py input.txt [output.prg]")
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else input_path.rsplit('.', 1)[0] + ".prg"
        convert_to_prg(input_path, output_path)
