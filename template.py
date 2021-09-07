import os

dirs_create = [os.path.join("data", "raw"),
        os.path.join("data","processed"),
        "notebooks",
        "saved_models",
        "src"
]
for dirs in dirs_create:
    os.makedirs(dirs, exist_ok=True)
    with open(os.path.join(dirs,".gitkeep"),'w') as f: # creating file inside folder
        pass
file = ["dvc.yaml", "src",
        "params.yaml", 
        ".gitignore",
        os.path.join("src","__init__.py")
    ]

for fi in file:
    with open(fi, 'w') as f:
        pass

