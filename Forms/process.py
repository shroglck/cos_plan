import os 
import pandas as pd 

shuffle=False 
blockworld = False

blockworld_all = False         
shuffle_all = False         
robo_all = False   
maze_all = True      
  

accuracy_shuffle = False


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
                    <p>Already performed Actions (q1: {file_index})</p>
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
                <p>Already performed Actions (q2: {file_index})</p>
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
    total_answered = {}
    for file_index in range(1,101):
        if file_index in [2, 42, 76, 84 ]:continue
        guessed = df_humans[f"Q{file_index}"].dropna()
        if len(guessed) == 0:continue 
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
            total_answered[file_index] = len(guessed)
            correct += (guessed == answer).sum()
            total += len(guessed)
    print(correct, total,  correct / total)
    print(len(total_answered), total_answered)
    # 23 48 0.4791666666666667
    # {3: 4, 5: 1, 12: 1, 13: 2, 14: 1, 16: 2, 18: 1, 25: 1, 26: 2, 28: 3, 32: 2, 33: 1, 34: 2, 35: 1, 37: 1, 44: 1, 47: 1, 49: 2, 54: 1, 55: 1, 56: 1, 58: 3, 59: 2, 69: 1, 72: 1, 79: 1, 82: 1, 88: 1, 89: 1, 91: 1, 94: 1, 96: 1, 97: 1, 98: 1}
    
                            
if maze_all:
    def conver_string_into_action(actions, template, padding='\t\t\t\t\t', change_colors=None):
        template += '\n'
        no_of_actions = len(actions.split('->')) - 1
        if no_of_actions == 1:
            if change_colors:
                template += f"{padding}<li {change_colors}>Step 1: {actions}</li>"
            else:
                template += f"{padding}<li>Step 1: {actions}</li>"
        else: 
            curr_ = 1 
            for action in actions.split(' , '): 
                if change_colors:
                    template += f"{padding}<li {change_colors}>Step {curr_}: {action.strip()}</li>\n"
                else:
                    template += f"{padding}<li>Step {curr_}: {action.strip()}</li>\n"
                curr_ += 1
        return template


    root='paths_correct'
    template = ""
    option_counter = 0 
    template += f"""
    <div class="all_maze">
    """
    for file_index in range(1,278):
        # if file_index in [14, 15]:continue
        if file_index in [15]:continue
        # print(file_index)
        image = f"q{file_index}.png"
        q_a = f"text_q{file_index}.txt"
        q_a = os.path.join(root, q_a)
        if not os.path.exists(q_a):continue 

        option_counter += 1
        template += f"""
        <div class="question_maze">
            <div >
                <img src='paths_correct/{image}' style="width: 40%;">
                <p style="font-style: italic;">(Q4: {file_index} / {option_counter}) Green needs to reach blue dot <br>
                Cells identified by its 0-indexed row and column (0,0 top left).<br> 
                Green dot <strong>can not</strong> bypass red dots <br>
                <strong>You can only move Green Dot to the next cell, via top, bottom, left and right movement</strong> (no digonal)<br>
                </p>
                <p class="already_done">Green dot will be moved as follows</p>
                <ul>"""
        already_found = None
        
        

        with open(q_a, "r") as f:
            Lines = f.readlines()
            for i,e in enumerate(Lines):
                e = e.strip()
                if 'already made along the path' in e:
                    # print(e)
                    already_found = True 
                    actions = e.split('path')[1]
                    
                    template = conver_string_into_action(actions, template, change_colors='class="already_done"')
                    break 

            template += f"""
            \t</ul>
            </div>\n"""

            # print(template)
            option_found = False 
            i+=1
            while i < len(Lines):
                line = Lines[i].strip()

                if 'Options are given as' not in line:
                    i+=1
                    continue 
                
                # print(line)
                options = line.split("{")[1]
                # options = "{" + options
                options = options.split("}")[0]
                # options += '}'

                option_found = None 
                option_dict = {}
                do_nothing = None 
                for e in options.split("'"):
                    if e == '' or e == ', ' or e == ': ':continue 
                    e = e.strip()
                    # print(e)
                    if e in ['A', 'B', 'C', 'D']:
                        if option_found:
                            if do_nothing:assert False 
                            option_dict[option_found] = 'Do nothing'
                            do_nothing = True 
                        option_found = e
                    else:
                        option_dict[option_found] = e 
                        option_found = None 
                
                Q_index = f"P4 : Q{option_counter}"
                for option in ['A', 'B', 'C', 'D']:
                    id = f"q4:{option_counter}{option}"
                    template += f'\t\t\t<input type="radio" id="{id}" name="{Q_index}" value="{option}">\n'
                    template += f'\t\t\t<label for="{id}"> Option {option}\n'
                    template += '\t\t\t\t<ul>'
                    template = conver_string_into_action(option_dict[option], template, padding='\t\t\t\t\t')
                    template += '\t\t\t\t</ul>\n\t\t\t</label>\n'
                break 
            template += '\t\t</div>\n'
            # print(template)
    template += '\t</div>'      
    with open('html_code_for_maze', "w") as f:
        f.write(template)
        
if blockworld_all:
    root='blockworld_e_final'
    template = ""

    template += f"""
    <div class="all_block">
    """

    for file_index in range(1,101):
        # if file_index in [3, 11, 22, 26, 39, 44, 58, 62, 71, 75, 88, 89, 92, 97, 99 ]:continue
        # if file_index in [2, 42, 76, 84 ]:continue
        # print(file_index)
        image = f"q{file_index}.png"
        q_a = f"text_q{file_index}.txt"
        q_a = os.path.join(root, q_a)

        template += f"""
        <div class="question_block">
            <div>
                <img src='blockworld_e_final/{image}' style="width: 100%;">
                <p style="font-style: italic;">(Q1: {file_index}) Blocks initial arrangemnet on left and final desired arrangemnet on the right. <br>
				Block uniquely identified by its ID and 0-indexed column (x axis, 0,1,2,3,4).  <br>
                Blocks can only be moved if there are no blocks above them <br>
                Blocks must be placed either on an empty column or on top of another block<br>
                Some steps may be wrong / infeasible 
                </p>
                <p class="already_done"> Blocks (on the image on left) will be moved as follows: </p>
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
                    template += f"\n\t\t\t\t\t<li class='already_done'>Step {e}</li>"
                    
                    
            template += f"""
            \t</ul>
            </div>\n"""
            
            # print(template)
            assert already_found == True 

            option_found = False 
            i+=1
            Q_index = f"P1 : Q{file_index}"
            while i < len(Lines):
                line = Lines[i].strip()
                if 'Option' in line and '[Options]' not in line:
                    i+=1
                    if option_found:
                        template += '\t\t\t</ul>\n\t\t\t</label>\n'
                    option_found = True 
                    option = line.split('Option')[1].strip()
                    option = option.replace(":", "")
                    id = f"q1:{file_index}{option}"
                    template += f'\t\t\t<input type="radio" id="{id}" name="{Q_index}" value="{option}">\n'
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
    template += '\t</div>'
    with open('html_code_for_block_all', "w") as f:
        f.write(template)
  
if shuffle_all:
    root='shuffle_e_final'
    template = ""
    template += f"""
    <div class="all_shuffle">
    """

    for file_index in range(1,101):
        # if file_index in [3, 11, 22, 26, 39, 44, 58, 62, 71, 75, 88, 89, 92, 97, 99 ]:continue
        if file_index in [2, 42, 76, 84 ]:continue
        # print(file_index)
        image = f"q{file_index}.png"
        q_a = f"text_q{file_index}.txt"
        q_a = os.path.join(root, q_a)

        template += f"""
            <div class="question_shuffle">
                <div >
                    <img src='shuffle_e_final/{image}' style="width: 100%;">
                    <p style="font-style: italic;"> (Q2: {file_index}) Swap patches on the left to generate image on the right. <br>
                    Patches identified by its 0-indexed Row and Column. 
                    For example, (0,2) is the top right on 0th row & 2nd column (columns are also 0,1,2) <br>
                    (0,0) top left &  2,2 is bottom right  <br>
                    </p>
                    <p class="already_done">Patches that will be swapped on image of the left</p>
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
                    template += f"\t\t\t\t<li class='already_done'>Step 1: {step_1}</li>\n"
                elif already_found:
                    step_n = e.strip()
                    template += f"\t\t\t\t\t<li class='already_done'>{step_n}</li>\n"

            template = template.split('select the correct option')[0]        
            template += f"""
            \t    </ul>
            \t</div>\n"""
            
            # print(template)
            assert already_found == True 

            option_found = False 
            i+=1
            Q_index = f"P2 : Q{file_index}"
            while i < len(Lines):
                line = Lines[i].strip()
                if 'Select the correct' in line: break 
                if  line == '' and i != len(Lines) - 1:
                    if option_found:
                        template += '\t\t\t\t\t</ul>\n\t\t\t\t</label>\n'
                    option_found = False 
                    i+=1
                    line = Lines[i].strip()
                    option = line.replace(".", "")
                    id = f"q2:{file_index}{option}"
                    template += f'\t\t\t\t<input type="radio" id="{id}" name="{Q_index}" value="{option}">\n'
                    template += f'\t\t\t\t<label for="{id}"> Option {option}\n'
                    template += '\t\t\t\t\t<ul>\n'
                    
                else:
                    option_found = True 
                    template += f'\t\t\t\t\t\t<li>{line}</li>\n'
                i +=1
            
            template += '\t\t\t\t\t</ul>\n\t\t\t\t</label>\n'
            template += '\t\t\t</div>'
            # print(template)
        
        template += '\n'
        # print(template)
    template += '\t</div>'      
    with open('html_code_for_shuffle_all', "w") as f:
        f.write(template)
    
if robo_all:
    root='robovqa_correct_finl'
    template = ""
    template += f"""
    <div class="all_robo">
    """
    option_counter = 0 
    for file_index in range(1,301):
        # if file_index in [2, 42, 76, 84 ]:continue
        # print(file_index)
        image = f"q{file_index}.png"
        image = f'robovqa_correct_finl/{image}'
        q_a = f"text_q{file_index}.txt"
        q_a = os.path.join(root, q_a)
        if not os.path.exists(image):continue 

        option_counter += 1        
        template += f"""
            <div class="question_robo">
                <div>
                    <img src='{image}' style="width: 100%;">
                    <p style="font-style: italic;">(Q3: {file_index} / {option_counter}) 
                    Robot / Hand will move objects and rearrange them in the scene. <br>
                    Desired arrangmenet of block on the right.<br>
                    </p>
                    <p class="already_done"> Actions that will be performed on left image</p>
                    <ul>\n"""

        already_found = None
        with open(q_a, "r") as f:
            Lines = f.readlines()
            for i,e in enumerate(Lines):
                e = e.strip()
                if e == '':continue 
                # print(e)
                if "robot has completed these steps:" in e:
                    already_found = True 
                elif 'A:' in e:break 
                elif already_found:
                    split =e.split(".") 
                    if len(split) == 3:
                        step_count, step_n, _ = split
                    else:
                        step_count, step_n= split
                    step_n = step_n.strip()
                    template += f"\t\t\t\t\t\t<li class='already_done'>Step {step_count}: {step_n}</li>\n"
                

            template = template.split('select the correct option')[0]        
            template += f"""\t\t\t\t\t</ul>
            \t</div>\n"""
            # print("=-=-")
            # print(template)
            first_option= True 
            assert already_found == True 
            Q_index = f"P3 : Q{option_counter}"
            # option_mapper = {'A':1, 'B':2, 'C':3, 'D':4}
            while i < len(Lines):
                line = Lines[i].strip()
                if line == '':
                    i+=1
                    continue  
                if 'Select the best option.' in line: break 
                # print(line)
                step_count, step_n= line.split(":")
                # option = option_mapper[step_count]
                option = step_count
                if not first_option:
                    template += f'\t\t\t\t\t</ul>\n'

                id = f"q3:{option_counter}{option}"
                template += f'\t\t\t\t<input type="radio" id="{id}" name="{Q_index}" value="{option}">\n'
                template += f'\t\t\t\t<label for="{id}"> Option {option}\n'
                template += f'\t\t\t\t\t<ul>\n'
                template += f'\t\t\t\t\t\t<li>{step_n}</li>\n'
                first_option = False 
                i+=1

            template += '\t\t\t\t\t</ul>\n\t\t\t\t</label>\n'
            template += '\t\t\t</div>'
            template += '\n'
            # print(template)
    template += '\t</div>'      
    with open('html_code_for_robo_all', "w") as f:
        f.write(template)
    


# cd ~/Downloads/Submission/"CosPlan (Shresth) CVPR'26"
# cd cos_plan/Forms/
# python process.py            

