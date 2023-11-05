#https://www.geeksforgeeks.org/numpy-vector-multiplication/
import numpy as np
import time
import pickle

class VecorialComparison:
    def __init__(self, WEdict = "glove") -> None:
        """_summary_

        Args:
            WEdict (str, optional): Word2Vec dict files from ["glove","enwiki"] or specify the path. Defaults to "glove".
        """
        if WEdict == "glove":
            
            dict_path = __file__.removesuffix("WE_vectorial_comparison_class.py")+"Word2VecPreloaded\\WEglove_dict.pkl"  #__file__+... permet de récupérer le fichier depuis Initializer et non ELIZA_APP
        elif WEdict == "enwiki":
            dict_path = __file__.removesuffix("WE_vectorial_comparison_class.py")+"Word2VecPreloaded\\WEenwiki_dict.pkl"
        else:
            dict_path = __file__.removesuffix("WE_vectorial_comparison_class.py")+"Word2VecPreloaded\\"+"WE"+WEdict+"_dict.pkl"
        
        print("Loading files...")
        time.sleep(0.5)
        begin = time.time()

        with open(dict_path,"rb") as f:
            self.dicVec = pickle.load(f)
        print("Loaded in",round(time.time()-begin,3),"seconds") #5 secondes pour charger les données
    
    def cosineSimilarity(self, word1 = str, word2 = str, correction = None) -> float:
        """_summary_

        Args:
            source (dict): _description_. Put the file loaded with pickle (word_embeded_dict.pkl).
            word1 (_str_): _description_ word n°1.
            word2 (_str_): _description_ word n°2.

        Returns:
            float: _description_ Compute cosine similarity with the formula A∙B/(||A||∙||B||)
        """

        if word1 not in self.dicVec.keys() or word2 not in self.dicVec.keys(): #Si le mot n'est pas dans le dictionnaire alors on retourne None
            return None
        
        vec1 = np.array(list(map(float,self.dicVec[word1].split(" ")))) #On convertie les mots en matrice de 100 ligne et 1 colonne (vecteur colonne)
        vec2 = np.array(list(map(float,self.dicVec[word2].split(" "))))
    
        dot_prod = np.dot(vec1,vec2) #euclidian dot product A∙B = Σa₁b₁
        vecnorm1 = np.linalg.norm(vec1)
        vecnorm2 = np.linalg.norm(vec2) #magnitude // norme du vecteur
    
        cosine_similarity = dot_prod/(vecnorm1*vecnorm2) #https://en.wikipedia.org/wiki/Cosine_similarityimport 

        if correction is None: #S'il n'y a pas de correction à appliquer on renvoit le cosinus
            return(cosine_similarity)
        else:
            autorized_character = ['X','Y','I','E','A','O','*','/','+','-','=','(',')',' ','.','>','<','!'] 
            autorized_character.extend([str(i) for i in range(0,10)]) #Pour des raisons de sécurité, seul ces caractères sont autorisés
            if [i in autorized_character for i in correction].count(False) >= 1: #Si un caractère n'est pas autorisé, on renvoie le cosinus sans corrections
                return(cosine_similarity)
            else:
                _locals = locals() #dictionnaire des variables locales
                correction = correction.replace("Y","cosine_similarity_corrected") 
                correction = correction.replace("X","cosine_similarity")
                correction = correction.replace("I","if")
                correction = correction.replace("E","else") 
                correction = correction.replace("A","and")
                correction = correction.replace("O","or")
                exec(correction, globals(), _locals) #On fait la correction et on met le résultat dans cos corrected du dictionnaire _locals
                cosine_similarity = _locals.pop("cosine_similarity_corrected")
                return cosine_similarity #On renvoie le résultat corrigé

    def maxCosineSimilarity(self, keys_list, word, correction):
        maxCosine = 0
        bestKey = ""
        
        for pop_elem in ["xnone","xforeign"]: #On retire les élements problématiques
            keys_list.pop(keys_list.index(pop_elem))
        
        for key in keys_list:
            cosine = self.cosineSimilarity(key.rstrip(),word,correction)
            if cosine is None: #Si le mot n'existe pas on ne le prend pas
                return None
            maxCosine = cosine if cosine > maxCosine else maxCosine #On remplace si le cos est plus grand
            if self.cosineSimilarity(key.rstrip(),word,correction) == maxCosine:
                bestKey = key.rstrip()
        
        return [bestKey, maxCosine]

    def getVector(self,word):
        return np.array(list(map(float,self.dicVec.get(word).split(" ")))) if self.dicVec.get(word) is not None else None

def main():
    test = VecorialComparison("gpt-2")
    while True:
        text = input("Expression 1 : ")
        if text == "--0--":
            break
        else:
            print(test.cosineSimilarity(text,input("Expression 2 : "), correction = "Y = (X-0.99)*100 I X > 0.99 E X"))

if __name__ == "__main__":
    main()