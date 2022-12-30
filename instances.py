class Clothes:
    def __init__(self, uc):
        self.undieColour = uc

    def wash(self):
        if self.undieColour is "black":
            return True
        else:
            return False


def main():
    lc = Clothes("pink")
    dc = Clothes("black")

    print("Dad wash?", dc.wash())
    print("Laura wash?", lc.wash())

if __name__ == "__main__":
    main()