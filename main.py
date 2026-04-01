from views.app import App
import sys
import os
import traceback

# garantir que o diretório do script esteja no path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        error_msg = f"Erro fatal:\n{e}\n\n{traceback.format_exc()}"
        try:
            import tkinter.messagebox as mb
            mb.showerror("Switch Focus — Erro", error_msg)
        except Exception:
            print(error_msg, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
