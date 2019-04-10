if __name__ == "__main__":
    g = lambda a,b: list(pow(i,2) for i in range(a,b+1))

    scores = [("Steve",10),("Anna",9),("Natalie",8)]

    f = lambda scores : sorted(scores, key=lambda score : score[1])

    print(g(30,50))
    print(f(scores))