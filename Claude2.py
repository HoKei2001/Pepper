from claude import Claude

def newClaude():
    cookie = "__ssid=148f790ebc4a057383c1ab278a7a22b; __stripe_mid=589047e1-6823-46b2-9333-119bdda2df3da9fd6e; sessionKey=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; intercom-device-id-lupk8zyo=0e888791-6cd6-4a34-87f9-0f753624a220; activitySessionId=1f220621-f704-4740-bb03-729dcd8efb4f; __cf_bm=9mQLaeNbIJWXQ_kDNN7XVNr4Q1gUlqAQPZ1BtS739OE-1698816164-0-AZdO6W8Z1C4gwF672C86sTIVmGTpD5muCbjyN7CIY4F3MVGL9UoK9Gdk5AkRz6egtZf3pXHSD1vg0TV1NcnKItc=; cf_clearance=PeA.JXRpD9bsnOf_f2xVOpDkG3Bx_Nmf7nRkQmwKs8I-1698816164-0-1-d90eee35.e41cbf9f.8e0fb1d5-0.2.1698816164; __stripe_sid=fac2bc84-aa6d-485b-bb8d-94896c2e976ffb94e2; intercom-session-lupk8zyo=N3BGU2VGNmRhcTIxdmVxT0JNcGwzQWpOeXZFeDhsMTNjZXdlSGdqTHRCSkxNWkx4VERjSjhkQWlJSEdGcStpNC0tZ1BzNXZkOFFkYmlOZjhkOGNiM3Ywdz09--f2daee8a556922afb76caefff7fa2b5b0d235c5e"
    claude = Claude(cookie)
    claude.create_new_conversation()
def Claude2bot(mmd_path, question):
    with open(mmd_path, 'r', encoding='utf-8') as file:
        paper_text = file.read()
    cookie = "__ssid=148f790ebc4a057383c1ab278a7a22b; __stripe_mid=589047e1-6823-46b2-9333-119bdda2df3da9fd6e; sessionKey=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; intercom-device-id-lupk8zyo=0e888791-6cd6-4a34-87f9-0f753624a220; activitySessionId=1f220621-f704-4740-bb03-729dcd8efb4f; __cf_bm=9mQLaeNbIJWXQ_kDNN7XVNr4Q1gUlqAQPZ1BtS739OE-1698816164-0-AZdO6W8Z1C4gwF672C86sTIVmGTpD5muCbjyN7CIY4F3MVGL9UoK9Gdk5AkRz6egtZf3pXHSD1vg0TV1NcnKItc=; cf_clearance=PeA.JXRpD9bsnOf_f2xVOpDkG3Bx_Nmf7nRkQmwKs8I-1698816164-0-1-d90eee35.e41cbf9f.8e0fb1d5-0.2.1698816164; __stripe_sid=fac2bc84-aa6d-485b-bb8d-94896c2e976ffb94e2; intercom-session-lupk8zyo=N3BGU2VGNmRhcTIxdmVxT0JNcGwzQWpOeXZFeDhsMTNjZXdlSGdqTHRCSkxNWkx4VERjSjhkQWlJSEdGcStpNC0tZ1BzNXZkOFFkYmlOZjhkOGNiM3Ywdz09--f2daee8a556922afb76caefff7fa2b5b0d235c5e"
    claude = Claude(cookie)

    prompt = (f"here is a scientific article : {paper_text} "
              f"Answer me the question: {question}"
              f"You should beautify your answer and only give me HTML"
              )
    response = claude.get_answer(prompt)
    print(response)

    return response


if __name__ == '__main__':
    Claude2bot()
