# 1. Ajoute le PPA
sudo add-apt-repository ppa:deadsnakes/ppa

# 2. Met à jour les dépôts
sudo apt update

# 3. Installe Python 3.13
sudo apt install python3.13 python3.13-venv python3.13-dev



# 1. HORS du venv — dans ton OS
sudo apt install python3.13 python3.13-venv python3.13-dev

# 2. Supprime l'ancien venv cassé
rm -rf ../venv_blog

# 3. Recrée avec Python 3.13
python3.13 -m venv ../venv_blog

# 4. Active
source ../venv_blog/bin/activate

# 5. Réinstalle les dépendances
pip install -r requirements.txt
