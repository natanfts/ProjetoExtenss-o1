from views.app import App
import sys
import os

# garantir que o diretório do script esteja no path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
