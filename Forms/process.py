import os 
import pandas as pd 

shuffle=False 
blockworld = False
accuracy_shuffle = True 

if shuffle:
    root='shuffle_e_final'
    template = ""
    for file_index in range(1,101):
        # if file_index in [3, 11, 22, 26, 39, 44, 58, 62, 71, 75, 88, 89, 92, 97, 99 ]:continue
        if file_index in [2, 42, 76, 84 ]:continue
        print(file_index)
        image = f"q{file_index}.png"
        q_a = f"text_q{file_index}.txt"
        q_a = os.path.join(root, q_a)

        template += f"""
            <div class="question">
                <div class="already_done">
                    <img src='shuffle_e_final/{image}' style="width: 100%;">
                    <p>Already performed Actions (q{file_index})</p>
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
                    template += f"\t\t\t\t<li>Step 1: {step_1}</li>\n"
                elif already_found:
                    step_n = e.strip()
                    template += f"\t\t\t\t\t<li>{step_n}</li>\n"

            template = template.split('select the correct option')[0]        
            template += f"""
            \t    </ul>
            \t</div>\n"""
            
            # print(template)
            assert already_found == True 

            option_found = False 
            i+=1
            while i < len(Lines):
                line = Lines[i].strip()
                if 'Select the correct' in line: break 
                if  line == '' and i != len(Lines) - 1:
                    if option_found:
                        template += '\t\t\t\t</ul>\n\t\t\t</label>\n'
                    option_found = False 
                    i+=1
                    line = Lines[i].strip()
                    option = line.replace(".", "")
                    id = f"q{file_index}{option}"
                    
                    template += f'\t\t\t<input type="radio" id="{id}" name="Q{file_index}" value="{option}">\n'
                    template += f'\t\t\t<label for="{id}"> Option {option}\n'
                    template += '\t\t\t\t<ul>\n'
                    
                else:
                    option_found = True 
                    template += f'\t\t\t\t\t<li>{line}</li>\n'
                i +=1
            
            template += '\t\t\t\t</ul>\n\t\t\t</label>\n'
            template += '\t\t</div>'
            # print(template)
        
        template += '\n'
        # print(template)
            
    with open('html_code_for_qa', "w") as f:
        f.write(template)
    
    

if blockworld:
    root='blockworld_e_final'
    template = ""
    for file_index in range(1,101):
        # if file_index in [3, 11, 22, 26, 39, 44, 58, 62, 71, 75, 88, 89, 92, 97, 99 ]:continue
        # if file_index in [2, 42, 76, 84 ]:continue
        print(file_index)
        image = f"q{file_index}.png"
        q_a = f"text_q{file_index}.txt"
        q_a = os.path.join(root, q_a)

        template += f"""
        <div class="question">
            <div class="already_done">
                <img src='blockworld_e_final/{image}' style="width: 100%;">
                <p>Already performed Actions (q{file_index})</p>
                <ul>"""
        already_found = None
        with open(q_a, "r") as f:
            Lines = f.readlines()
            for i,e in enumerate(Lines):
                e = e.strip()
                if '[Target Configuration]' in e:break 
                if e == "[Previously Executed Moves]":
                    already_found = True 
                    continue 
                if e == 'The following moves were correctly executed:':continue 
                if already_found and '.' in e:
                    template += f"\n\t\t\t\t\t<li>Step {e}</li>"
                    
                    
            template += f"""
            \t</ul>
            </div>\n"""
            
            # print(template)
            assert already_found == True 

            option_found = False 
            i+=1
            while i < len(Lines):
                line = Lines[i].strip()
                if 'Option' in line and '[Options]' not in line:
                    i+=1
                    if option_found:
                        template += '\t\t\t</ul>\n\t\t\t</label>\n'
                    option_found = True 
                    option = line.split('Option')[1].strip()
                    option = option.replace(":", "")
                    id = f"q{file_index}{option}"
                    template += f'\t\t\t<input type="radio" id="{id}" name="Q{file_index}" value="{option}">\n'
                    template += f'\t\t\t<label for="{id}"> Option {option}\n'
                    template += '\t\t\t<ul>\n'
                    while i < len(Lines):
                        line = Lines[i].strip()    
                        if 'Option' in line or line =='':break 
                        template += f'\t\t\t\t<li>{line}</li>\n'
                        i+=1

                i+=1
            template += '\t\t\t</ul>\n\t\t\t</label>\n'
            template += '\t\t</div>'
            # print(template)
            
        template += '\n'
        # print(template)
    with open('html_code_for_block', "w") as f:
        f.write(template)
    
    
if accuracy_shuffle:
    df_humans = pd.read_csv('accuracy_shuffle.csv')
    
    root='shuffle_e_final'
    solutions = {}
    correct = 0 
    total = 0 
    for file_index in range(1,101):
        if file_index in [2, 42, 76, 84 ]:continue
        print(file_index)
        q_a = f"text_q{file_index}.txt"
        q_a = os.path.join(root, q_a)
        with open(q_a, "r") as f:
            Lines = f.readlines()
            for i,e in enumerate(Lines):
                if 'Correct Answer:' not in e:
                    continue 
                solutions[file_index] = e.split('Correct Answer: ')[1]
                answer = solutions[file_index] 
            guessed = df_humans[f"Q{file_index}"].dropna()
            correct += (guessed == answer).sum()
            total += len(guessed)
    import pdb
    pdb.set_trace()
    print(correct, total,  correct / total)
            
            
    
                            
    

# cd cos_plan/Forms/
# python process.py            

