import os 

root='shuffle_e_final'
template = ""
for file_index in range(1,101):
    if file_index in [3, 11, 22, 26, 39, 44, 58, 62, 71, 75, 88, 89, 92, 97, 99 ]:continue
    print(file_index)
    image = f"q{file_index}.png"
    q_a = f"text_q{file_index}.txt"
    q_a = os.path.join(root, q_a)

    template += f"""
        <div class="question">
            <div class="already_done">
            <img src='shuffle_e_final/{image}' style="width: 100%;">
            <p>Already performed Actions</p>
            <ul>
    """
    already_found = None
    with open(q_a, "r") as f:
        Lines = f.readlines()
        for i,e in enumerate(Lines):
            if 'Options:' in e:break 
            if "Following steps have already been taken" in e:
                already_found = True 
                step_1 = e.split('Step 1:')[1].strip()
                template += f"\t\t<li>Step 1: {step_1}</li>\n"
            elif already_found:
                step_n = e.strip()
                template += f"\t\t<li>{step_n}</li>\n"

        template = template.split('select the correct option')[0]        
        template += f"""
            </ul>
        </div>"""
        
        # print(template)
        assert already_found == True 

        option_found = False 
        i+=1
        while i < len(Lines):
            line = Lines[i].strip()
            if 'Select the correct' in line: break 
            if  line == '' and i != len(Lines) - 1:
                if option_found:
                    template += '\t  </ul>\n\t</label>\n'
                option_found = False 
                i+=1
                line = Lines[i].strip()
                option = line.replace(".", "")
                id = f"q1{option}"
                
                template += f'\t<input type="radio" id="{id}" name="Q{file_index}" value="{option}">\n'
                template += f'\t<label for="{id}"> Option {option}\n'
                template += '\t  <ul>\n'
                
            else:
                option_found = True 
                template += f'\t\t<li>{line}</li>\n'
            i +=1
        
        template += '\t  </ul>\n\t</label>\n'
        template += '\t</div>'
        # print(template)
    
    template += '\n\n'
    # print(template)
        



with open('html_code_for_qa', "w") as f:
    f.write(template)
    
    

# python process.py            

