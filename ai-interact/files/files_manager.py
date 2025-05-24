from io import BytesIO

class FilesManager:

    @staticmethod
    def get_mine_type_from_file_name(file_name: str) -> str:
        """
        Returns the mime type of a file based on its extension.
        """
        if file_name.endswith('.txt'):
            return 'text/plain'
        elif file_name.endswith('.py'):
            return 'text/x-python'
        elif file_name.endswith('.js'):
            return 'application/javascript'
        elif file_name.endswith('.ts'):
            return 'application/typescript'
        elif file_name.endswith('.java'):
            return 'text/x-java-source'
        elif file_name.endswith('.cs'):
            return 'text/x-csharp'
        elif file_name.endswith('.fs'):
            return 'text/x-fsharp'
        elif file_name.endswith('.css'):
            return 'text/css'
        elif file_name.endswith('.scss'):
            return 'text/x-scss'
        elif file_name.endswith('.csv'):
            return 'text/csv'
        elif file_name.endswith('.pdf'):
            return 'application/pdf'
        elif file_name.endswith('.xlsx'):
            return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        elif file_name.endswith('.xls'):
            return 'application/vnd.ms-excel'
        elif file_name.endswith('.docx'):
            return 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif file_name.endswith('.doc'):
            return 'application/msword'
        elif file_name.endswith('.html'):
            return 'text/html'
        else:
            return 'application/octet-stream'