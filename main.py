import os,yaml
import argparse


RECIPE_ROOT = os.path.join(os.path.dirname(__file__),'recipes')

def get_default_command(default_yaml_path,debug=False):
    
    with open(default_yaml_path, 'r') as f:
        default_yaml = yaml.load(f, Loader=yaml.FullLoader)
    if debug:
        args_template = default_yaml['DEBUG']
    else:
        args_template = default_yaml['TRAIN']
    return args_template

def setup_exp(exp_folder,args_template,debug=False):
    # copy the args_template
    args_ = args_template.copy()
    python_command = 'python -u {}'.format(args_['train_script_path'])
    args_.pop('train_script_path')
    
    # read the config.yaml file
    config_path = os.path.join(exp_folder,'config.yaml')
    with open(config_path, 'r') as f:
        config_yaml = yaml.load(f, Loader=yaml.FullLoader)
    
    # update the args_ for every exp
    network_name = args_['output_name']
    for exp in config_yaml:
        python_command_ = python_command
        name = exp['name']
        output_dir = os.path.join(exp_folder,name)
        os.makedirs(output_dir,exist_ok=True)
        args_.update({'output_dir':output_dir})
        
        exp_name = exp_folder.split('\\')[-1]
        args_.update({'output_name':network_name+'_'+exp_name+'_'+name})
        exp.pop('name')
        for k,v in exp.items():
            args_.update({k:v})
        # write the config to the config.yaml file
        with open(os.path.join(output_dir,'config.yaml'),'w') as f:
            yaml.dump(args_,f)
        
        for k,v in args_.items():
            if v is True:
                arg_ = '--{}'.format(k)
            elif v == False:
                continue
            else:
                arg_ = '--{} {}'.format(k, v)
            python_command_ += ' {}'.format(arg_)
        # write the command to the run.sh file
        if debug:
            with open(os.path.join(output_dir,'run_debug.sh'),'w') as f:
                f.write(python_command_)
        else:
            with open(os.path.join(output_dir,'run.sh'),'w') as f:
                f.write(python_command_)
    return True
    

def setup_recipes(recipe,debug=False):
    recipe_path = os.path.join(RECIPE_ROOT,recipe)
    default_yaml_path = os.path.join(recipe_path, 'default.yaml')
    args_template = get_default_command(default_yaml_path,debug=debug)
    # list all the folder in the recipe
    folder_list = os.listdir(recipe_path)
    folder_list.remove('default.yaml')
    for folder in folder_list:
        folder = os.path.join(recipe_path,folder)
        setup_exp(folder,args_template,debug=debug)

def run_exp(exp_path,debug=False):
    run_sh_path = os.path.join(exp_path,'run.sh')
    if debug:
        run_sh_path = run_sh_path.replace('run.sh','run_debug.sh')
    
    command = open(run_sh_path,'r').read()
    return os.system(command)

def run_recipe(recipe,debug=False,only_exp=None):
    recipe_path = os.path.join(RECIPE_ROOT,recipe)
    folder_list = os.listdir(recipe_path)
    folder_list.remove('default.yaml')
    if only_exp is not None:
            folder_list = [only_exp]
            
    for folder in folder_list:
        exp_list = os.listdir(os.path.join(recipe_path,folder))
        exp_list.remove('config.yaml')
        
        for exp in exp_list:
            print(f'Running {os.path.join(recipe_path,folder,exp)}')
            code = run_exp(os.path.join(recipe_path,folder,exp),debug=debug)
            if debug and code!=0:
                print('Error in {}'.format(os.path.join(recipe_path,folder,exp)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--recipe', type=str, required=True) # recipe name / recipe的名字
    parser.add_argument('--exp', type=str, default=None) # if you don't want to run all the exps in the recipe, you can specify the exp name / 如果你不想运行recipe中的所有实验，你可以指定实验的名字
    parser.add_argument('--debug', action='store_true') # if you want to run the debug mode to run the recipe with mini datasets / 如果你想运行debug模式
    args = parser.parse_args()
    setup_recipes(args.recipe,debug=args.debug)
    run_recipe(args.recipe,debug=args.debug,only_exp=args.exp)