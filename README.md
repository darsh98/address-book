# address-book

# after clone the repository following this steps

# create virtual enviorment
python -m venv venv

# activa virtual enviorment
for windows
cd venv/Scripts/activate

for ubuntu
source venv/bin/activate    

# install requirement.txt
pip install requirement.txt

# run the application
uvicorn main:app --reload