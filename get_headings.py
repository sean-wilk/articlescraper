# function to get headings as I want them
def get_headings(heading,row,word_limit = 0,add_text_end="",add_bracket_end=""):

    x_text = row.find_all(heading)
    x = []

    for text in x_text:
        text = text.get_text(' ', strip=True)
        x.append(text)

    if word_limit > 0:
        limit_text = ' '.join(x)
        limit_list = limit_text.split(" ")
        if ' '.join(limit_list[:word_limit]) != "":
            x_string = "<" + heading + ">" + ' '.join(limit_list[:word_limit]) + add_text_end + "</" + heading + ">" + add_bracket_end
        else:
            x_string = ""
    else:
        if ' '.join(x) != "":
            x_string = "<" + heading + ">" + ' '.join(x) + add_text_end + "</" + heading + ">" + add_bracket_end
        else:
            x_string = ""

    return x_string;
