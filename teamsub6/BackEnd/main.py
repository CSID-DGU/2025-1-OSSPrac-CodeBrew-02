from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 세션 사용을 위해 필요


def mask_email(email):
    if "@" in email:
        name, domain = email.split("@")
        return name[0] + "***@" + domain
    return email


def mask_phone(phone):
    if "-" in phone:
        parts = phone.split("-")
        if len(parts) == 3:
            return f"{parts[0]}-****-{parts[2]}"
    return phone

# 메인 페이지


@app.route('/')
def index():
    session.pop('result', None)  # 세션에 저장된 결과 초기화
    result = session.get('result', [])  # 세션에서 결과 데이터를 가져옴
    # 결과 데이터를 index.html로 전달
    return render_template('index.html', result=result)

# 학생 정보 입력 페이지 경로


@app.route('/input')
def input():
    return render_template('input.html')  # input.html 렌더링

# 제출된 데이터를 처리하여 출력하는 경로


@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        # 학생 정보 데이터를 각 리스트로 저장
        names = request.form.getlist('Name[]')
        roles = [request.form.get(f'Role[{i}]') for i in range(len(names))]
        student_numbers = request.form.getlist('StudentNumber[]')
        genders = [request.form.get(f'Gender[{i}]') for i in range(len(names))]
        majors = request.form.getlist('Major[]')
        languages = [', '.join(request.form.getlist(
            f'language[{i}][]')) for i in range(len(names))]
        emails = [f"{email}@{domain}" for email, domain in zip(
            request.form.getlist('Email[]'), request.form.getlist('EmailDomain[]'))]
        phones = request.form.getlist('Phone[]')
        mbtis = request.form.getlist('MBTI[]')

        # 선택된 사진 파일 처리
        pictures = [request.form.get(
            f'Picture[{i}]', '') for i in range(len(names))]
        picture_paths = {
            'Picture1': "https://raw.githubusercontent.com/CSID-DGU/2025-1-OSSPrac-CodeBrew-02/main/Subject3_2/images/member1.png",
            'Picture2': "https://raw.githubusercontent.com/CSID-DGU/2025-1-OSSPrac-CodeBrew-02/main/Subject3_2/images/member2.png",
            'Picture3': "https://raw.githubusercontent.com/CSID-DGU/2025-1-OSSPrac-CodeBrew-02/main/Subject3_2/images/member3.png",
        }
        selected_pictures = [picture_paths.get(
            picture, picture_paths['Picture1']) for picture in pictures]

        # 마스킹 적용
        masked_emails = [mask_email(e) for e in emails]
        masked_phones = [mask_phone(p) for p in phones]

        # 학생 정보 리스트 생성
        zipped_result = list(zip(names, roles, student_numbers, genders, majors,
                             languages, masked_emails, masked_phones, mbtis, selected_pictures))
        session['result'] = zipped_result  # 세션에 결과 저장

        # 결과 데이터를 result.html로 전달
        return render_template('result.html', result=zipped_result)

# 팀 연락정보 페이지


@app.route('/contact')
def contact_info():
    return render_template('contact.html')  # contact.html 렌더링


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
