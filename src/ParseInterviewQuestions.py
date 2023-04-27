import re
from joppy.api import Api

def parse_markdown_file(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        markdown_text = f.read()

    # Split the markdown text into individual question/answer pairs
    qa_pairs = re.findall(r"(?s)(?<=\n)# (.+?)\n\n(.+?)(?=\n# |\Z)", markdown_text)

    #print(qa_pairs)

    # 形成包含多个问答字典的列表
    result = []
    for qa_pair in qa_pairs:
        question = qa_pair[0]
        answer = qa_pair[1].strip()
        addition = ""

        result.append({
                "question": question,
                "answer": answer,
                "addition": addition
            })
    return result



def parse_markdown_joplin(token,note_id):
    api = Api(token=token)

    test_note = api.get_note(id_=note_id,fields="body")

    print(test_note)

    # Split the markdown text into individual question/answer pairs
    qa_pairs = re.findall(r"(?s)(?<=\n)# (.+?)\n\n(.+?)(?=\n# |\Z)", test_note.body)

    # 形成包含多个问答字典的列表
    result = []
    for qa_pair in qa_pairs:
        question = qa_pair[0]
        answer = qa_pair[1].strip()
        addition = ""

        result.append({
            "question": question,
            "answer": answer,
            "addition": addition
        })
    return result

if __name__ == "__main__":

    result = parse_markdown_joplin()

    # file_path = "C:/Users/admin/Desktop/多线程.md"
    #
    # result = parse_markdown_file(file_path)
    #
    print(result)
    print(result[0])
