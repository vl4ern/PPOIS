# README: Автомастерская (Car repair shop)

- Классы: 64
- Поля: 152
- Уникальные поведения: 114
- Ассоциации: 41
- Исключения: 12

## Исключения (12)
Находятся в exceptions

- StudentSystemError — базовое исключение.
- InvalidSelectionError — некорректный выбор.
- DuplicateIDError — дублированние информации.
- EnrollmentError — ошибка при зачислении.
- CourseNotFoundError — ошибка выбора курса.
- TeacherNotFoundError — ошибка выбора преподователя.
- TimeSlotUnavailableError — некорректный выбор даты.
- PaymentError — ошибка при опалте.
- AuthenticationError — ошибка аутентификации.
- InsufficientFundsError — ошибка при недостатке средств.
- LibraryError - ошибка поиска в библиотеке.
- HousingError - ошибка при выборе дома.

## Классы
Формат: Имя_класса Поля Методы -> Ассоциации (связанные классы/модули)

### Academic

Degree 3 1 -> requirement
- Поля: name, level, requirements
- Методы: add_requirement

Exam 2 1 -> 
- Поля: course, date
- Методы: schedule

GradeScale 1 1 ->
- Поля: mapping
- Методы: grade_to_letter

Program 3 1 -> Course
- Поля: code, title, courses
- Методы: add_course

Requirement 2 0 ->
- Поля: desc, credits
- Методы:

### Additional

Badge 2 1 ->
- Поля: name, level
- Методы: promote

Event 3 1 ->
- Поля: title, date, location
- Методы: describe

Notification 4 1 ->
- Поля: to, subject, body, sent
- Методы: send

RecoveryToken 3 1 ->
- Поля: user, token, used
- Методы: use

RolePerm  2 1 ->
- Поля: role, perms
- Методы: has

### Course 

Course 6 2 -> Modules, Schedule_options
- Поля: code, title, credits, syllabus, modules, schedule_options
- Методы: add_module, available_times

CourseSchedule 2 1 -> Course
- Поля: course, timeslot
- Методы: is_conflict

Module 2 1 ->
- Поля: name, lessons
- Методы: workload

Syllabus 2 1 ->
- Поля: summary, topics
- Методы: topic_count

### Account

Account 4 2 -> Transactions
- Поля: owner, balance, transactions, amount
- Методы: deposit, withdraw

Billing 3 1 -> Invoices
- Поля: invoices, owner, amount
- Методы: create_invoice

Card 4 2 -> Account
- Поля: account, card_number, holder_name, blocked
- Методы: block, unblock

Scholarship 3 1 -> 
- Поля: awardee, amount, reason
- Методы: award

Transaction 4 1 -> Card
- Поля: from_card, to_card, amount, reference
- Методы: execute

### Housing

Dorm 3 1 -> Room
- Поля: name, capacity, rooms
- Методы: vacancy

Lease 5 1 -> Room
- Поля: resident, room, start_date, end_date, date_str
- Методы: is_active

MaintenanceRequest 3 1 -> Room
- Поля: issue, room, status
- Методы: resolve

Room 4 1 -> 
- Поля: number, floor, occupied, resident
- Методы: assign

### Library

Author 2 1 ->
- Поля: name, born
- Методы: profile

Book 4 1 -> 
- Поля: title, author, isbn, available
- Методы: checkout

BorrowRecord 4 1 -> Book
- Поля: book, borrower, due_date, today_str
- Методы: is_overdue

Library 5 2 -> BorrowRecords
- Поля: name, address, catalog, borrow_records, title
- Методы: add_book, find_book

### Person 

Address 4 1 -> University
- Поля: street, city, zip_code, country
- Методы: formatted

ContactInfo 3 1 -> Theacher
- Поля: email, phone, alt_phone
- Методы: reachable

IDCard 3 1 -> Person
- Поля: uid, issued_by, valid_until
- Методы: is_valid

Person 5 2 -> Student, Teacher
- Поля: first_name, last_name, email, phone, metadata
- Методы: full_name, contact_card

### Scheldule

CalendarEntry 4 1 -> TimeSlot
- Поля: owner, timeslot, location, other
- Методы: conflicts_with

Scheduler 3 2 -> Entries
- Поля: entries, person, entry
- Методы: add_entry, find_entries_for

TimeSlot 4 1 -> 
- Поля: day, start, end, label
- Методы: describe

### Student

CalendarEntry 5 3 -> TimeSlot
- Поля: owner, timeslot, location, other, course
- Методы: conflicts_with, enroll, drop

EnrollmentRecord 3 1 -> Student
- Поля: student, course, status
- Методы: is_active

GradeRecord 3 0-> 
- Поля: course_code, grade, credits
- Методы:

Student 7 1 -> Person, EnrollmentRecord
- Поля: first_name, last_name, email, student_id, enrolled_courses, transcript, housing
- Методы: enroll

Transcript 2 2 -> Entries
- Поля: entries, grade_record
- Методы: add_grade, gpa

Office 3 1 -> 
- Поля: building, room, phone
- Методы: location

Qualification 3 1 -> 
- Поля: title, institution, year
- Методы: short

Teacher 7 3 -> Person, Course, Qualification
- Поля: first_name, last_name, teacher_id, email, courses, office, qualifications
- Методы: add_course, remove_course, profile

Campus 2 0 -> 
- Поля: location, capacity
- Методы: 

Department 4 1 -> Course
- Поля: name, head, courses, course
- Методы: add_course

Faculty 2 0 -> 
- Поля: name, dean
- Методы:

University 5 2 -> Departments, Campus
- Поля: name, departments, campuses, dept, code
- Методы: find_course, add_department

### service/behaviors

PaymentProcessor 8 2 -> Card
- Поля: log, card, cvv, card_number, from_card, to_card, amount, reference
- Методы: transfer, verify_card

BehaviorManager -> Behaviors
- Поля: behaviors, name, fn
- Методы: register, run_all

NotificationService 2 1 -> 
- Поля: notification, sent
- Методы: notify

LibraryAssistant 4 1 -> Library, Book, BorrowRecord
- Поля: library, book, borrower, br
- Методы: checkout_book

### service/registretion

Registrar 14 4 -> Student, Teacher, Course
- Поля: students, teachers, first_name, last_name, student_id, email, s, teacher, student_id, teacher_id, course_code, course, timeslot_index, record
- Методы: register_student, add_teacher, available_teachers, enroll_student