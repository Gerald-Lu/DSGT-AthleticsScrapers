from bs4 import BeautifulSoup

with open('home.html', 'r') as file:
    content = file.read()
    print(content)
    soup = BeautifulSoup(content, 'lxml')
    #courses = soup.find_all('h5')
    course_cards = soup.find_all('div', class_='card')
    for c in course_cards:
        course_name = c.h5.text
        course_price = c.a.text.split()[-1]
        print(f'{course_name} costs {course_price}')