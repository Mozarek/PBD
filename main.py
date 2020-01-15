import numbers
import random
import datetime

from faker import Faker

from data import *

fake = Faker()

allClients = list()
allConferences = list()
allConferenceDays = list()
allWorkshops = list()
allConferenceReservations = list()
allConferenceDayReservations = list()
allThresholds = list()
allParticipants = list()
allDayAdmissions = list()
allWorkshopReservations = list()
allWorkshopAdmissions = list()


def convertToSqlArgs(*argv):
    q = '('
    for arg in argv:
        if isinstance(arg, numbers.Number):
            q += str(arg) + ', '
        elif isinstance(arg, str):
            q += '\'' + arg + '\', '

    q = q[:-2]
    return q + ')'


def generateClients(number_of_clients):
    cols = '(name, phone, isCompany)'
    query = 'INSERT INTO [dbo].[Clients] ' + cols + ' VALUES '
    for i in range(number_of_clients):
        name = fake.company()
        phone = fake.phone_number()
        isCompany = random.randint(0, 1)
        allClients.append(Client(i + 1, name, phone, isCompany))
        query += convertToSqlArgs(name, phone, isCompany) + ', '
    return query[:-2]


def generateConferences(number_of_conferences, fromDate, daysDelta):
    cols = '(ConferenceName, Price, StudentDiscount, StartDate, EndDate)'
    query = 'INSERT INTO [dbo].[Conferences] ' + cols + ' VALUES '
    for i in range(number_of_conferences):
        name = fake.catch_phrase().split()[-1].capitalize() + \
               random.choice([' Days', ' Conference', ' Meet-up', 'Conf', ' Congress'])
        price = random.randint(3, 79) * 10
        studentDiscount = random.random()
        startDate = fromDate + datetime.timedelta(days=random.randint(0, daysDelta))
        endDate = startDate + datetime.timedelta(days=random.randint(0, 2))
        allConferences.append(Conference(i + 1, name, price, studentDiscount, startDate, endDate))
        query += convertToSqlArgs(name, price, studentDiscount, str(startDate), str(endDate)) + ', '
    return query[:-2]


def generateDiscountThresholds(maxThresholdsPerConference):
    cols = '(ConferenceID, StartDate, EndDate, Discount)'
    query = 'INSERT INTO [dbo].[DiscountThresholds] ' + cols + ' VALUES '

    i = 0
    for conf in allConferences:
        numberOfThresholds = random.randint(0, maxThresholdsPerConference)
        if numberOfThresholds == 0:
            break
        d = random.randint(numberOfThresholds*3, 60)
        firstDate = conf.startDate - datetime.timedelta(days=d)
        splittingDays = sorted(random.sample(range(1, d-1), numberOfThresholds-1))
        splittingDays.append(d)
        lastDay = 0
        for splitDay in splittingDays:
            discount = random.choice([random.random(), random.random(), random.random(), -random.random()])
            startDate = firstDate + datetime.timedelta(days=lastDay)
            endDate = firstDate + datetime.timedelta(days=splitDay)
            lastDay = splitDay
            allThresholds.append(DiscountThreshold(i+1, conf.id, startDate, endDate, discount))
            query += convertToSqlArgs(conf.id, str(startDate), str(endDate), str(discount)) + ', '
            i += 1
    return query[:-2]


def generateConferenceDays():
    cols = '(ConferenceID, Date, ParticipantLimit)'
    query = 'INSERT INTO [dbo].[ConferenceDays] ' + cols + ' VALUES '

    i = 0
    for conf in allConferences:
        numberOfDays = random.randint(0, 2)
        for j in range(numberOfDays):
            date = conf.startDate + datetime.timedelta(days=j)
            limit = random.randint(5, 200)
            allConferenceDays.append(ConferenceDay(i + 1, conf.id, date, limit))
            query += convertToSqlArgs(conf.id, str(date), limit) + ', '
            i += 1
    return query[:-2]


def generateWorkshops():
    cols = '(DayID , Name, StartTime, EndTime, ParticipantLimit, Price)'
    query = 'INSERT INTO [dbo].[Workshops] ' + cols + ' VALUES '

    i = 0
    for confDay in allConferenceDays:
        numberOfWorkshops = random.randint(0, 5)
        for j in range(numberOfWorkshops):
            name = random.choice([random.choice(['How to ', 'Deciding to ', 'Why I started to ']) + fake.bs(),
                                  random.choice(['The era of ', 'Novel approach to ', 'Pros and cons of ']) + " ".join(
                                      fake.bs().split()[1:])])
            start = datetime.time(hour=random.randint(9, 17), minute=random.randint(0, 11) * 5)
            end = datetime.time(hour=start.hour + random.randint(1, 4), minute=start.minute)
            limit = random.randint(3, confDay.limit)
            price = random.randint(1, 25) * 10
            allWorkshops.append(Workshop(i + 1, confDay.id, name, start, end, limit, price))
            query += convertToSqlArgs(confDay.id, name, str(start), str(end), limit, price) + ', '
            i += 1
    return query[:-2]


def generateConferenceReservations(maxReservationsPerConference):
    cols = '(ConferenceID, ClientID, ReservationDate)'
    query = 'INSERT INTO [dbo].[ConferenceReservations] ' + cols + ' VALUES '

    i = 0
    for conf in allConferences:
        reservationsNumber = random.randint(0, maxReservationsPerConference)
        clientsList = random.sample(allClients, min(reservationsNumber, len(allClients)))
        for client in clientsList:
            reservationDate = conf.startDate - datetime.timedelta(days=random.randint(0, 60))
            allConferenceReservations.append(ConferenceReservation(i + 1, conf.id, client.id, reservationDate))
            query += convertToSqlArgs(conf.id, client.id, str(reservationDate)) + ', '
            i += 1
    return query[:-2]


def generateDayReservations(maxReservationsPerDay):
    cols = '(DayID, ReservationID, ParticipantsNumber, StudentParticipantsNumber)'
    query = 'INSERT INTO [dbo].[DayReservations] ' + cols + ' VALUES '

    i = 0
    for day in allConferenceDays:
        conf = allConferences[day.confID - 1]
        reservations = list()
        for confReservation in allConferenceReservations:
            if confReservation.id == day.confID:
                reservations.append(confReservation)
        reservations = random.sample(reservations, min(maxReservationsPerDay, len(reservations)))
        for reservation in reservations:
            participants = random.randint(0, min(3 * day.limit / len(reservations), day.freePlaces))
            studentParticipants = random.randint(0, participants)
            thresholdDiscount = 0
            for t in allThresholds:
                if t.confID == conf.id and t.startDate <= reservation.registrationDate < t.endDate:
                    thresholdDiscount = t.discount
                    break
            toPay = (1 - thresholdDiscount) * (conf.price * (1 - conf.studentDiscount) * studentParticipants +
                                               conf.price * (participants - studentParticipants))
            reservation.toPay += toPay
            allConferenceDayReservations.append(
                DayReservation(i+1, day.id, reservation.id, participants, studentParticipants, toPay))
            query += convertToSqlArgs(day.id, reservation.id, participants, studentParticipants) + ', '
            i += 1
    return query[:-2]


def generateDayAdmissions():
    cols = '(ParticipantID, DayReservationID, isStudent)'
    queryStart = 'INSERT INTO [dbo].[DayAdmissions] ' + cols + ' VALUES '
    query = queryStart

    i = 0
    for dayReservation in allConferenceDayReservations:
        participantsNumber = dayReservation.participantsNumber
        dayParticipants = random.sample(allParticipants, min(participantsNumber, len(allParticipants)))
        for participant in dayParticipants:
            if i % 600 == 599:
                query += '\n' + queryStart
            isStudent = random.randint(0, 1)
            allDayAdmissions.append(DayAdmission(i+1, participant.id, dayReservation.id, isStudent))
            query += convertToSqlArgs(participant.id, dayReservation.id, isStudent) + ', '
            i += 1
    return query[:-2]


def generateParticipants(participantsNumber):
    cols = '(FirstName, LastName, EMailAddress)'
    queryStart = 'INSERT INTO [dbo].[Participants] ' + cols + ' VALUES '
    query = queryStart

    for i in range(0, participantsNumber):
        if i % 600 == 599:
            query += '\n' + queryStart
        name = fake.first_name()
        lastName = fake.last_name()
        email = fake.ascii_email()
        allParticipants.append(Participant(i+1, name, lastName, email))
        query += convertToSqlArgs(name, lastName, email) + ', '
    return query[:-2]


def generateWorkshopReservations():
    cols = '(WorkshopID, DayReservationID, ParticipantsNumber)'
    queryStart = 'INSERT INTO [dbo].[WorkshopReservations] ' + cols + ' VALUES '
    query = queryStart

    i = 0
    for workshop in allWorkshops:
        dayReservations = [dr for dr in allConferenceDayReservations if dr.dayID == workshop.dayID]
        for dayReservation in dayReservations:
            participantsNumber = random.randint(0, workshop.freePlaces)
            if participantsNumber == 0:
                continue
            workshop.freePlaces -= participantsNumber
            if i % 600 == 599:
                query += '\n' + queryStart
            allWorkshopReservations.append(WorkshopReservation(i+1, workshop.id, dayReservation.id, participantsNumber))
            query += convertToSqlArgs(workshop.id, dayReservation.id, participantsNumber) + ', '
            i += 1
    return query[:-2]


def generateWorkshopAdmissions():
    cols = '(WorkshopID, DayAdmissionID)'
    queryStart = 'INSERT INTO [dbo].[WorkshopAdmissions] ' + cols + ' VALUES '
    query = queryStart

    i = 0
    for dayAdmission in allDayAdmissions:
        workshopReservations = [w for w in allWorkshopReservations if w.dayReservationID == dayAdmission.dayReservationID]
        random.shuffle(workshopReservations)
        enrolledForWorkshops = list()
        for workshopReservation in workshopReservations:
            workshop = allWorkshops[workshopReservation.workshopID-1]
            canAttend = True
            if workshopReservation.notEnrolled == 0:
                canAttend = False
            for w in enrolledForWorkshops:
                if w.dayID == workshop.dayID and \
                        (workshop.start <= w.start <= workshop.end or workshop.start <= w.end <= workshop.end):
                    canAttend = False
                    break
            if not canAttend:
                continue
            workshopReservation.notEnrolled -= 1
            enrolledForWorkshops.append(workshop)
            if i % 600 == 599:
                query += '\n' + queryStart
            allWorkshopAdmissions.append(WorkshopAdmission(dayAdmission.id, workshopReservation.id))
            query += convertToSqlArgs(dayAdmission.id, workshopReservation.id) + ', '
            i += 1
    return query[:-2]


totalQuery = generateClients(5) + '\n' + \
             generateConferences(5, datetime.date(year=2010, month=1, day=1), 8 * 365) + '\n' + \
             generateDiscountThresholds(4) + '\n' + \
             generateConferenceDays() + '\n' + \
             generateWorkshops() + '\n' + \
             generateConferenceReservations(2) + '\n' + \
             generateDayReservations(3) + '\n' + \
             generateParticipants(100) + '\n' + \
             generateDayAdmissions() + '\n' + \
             generateWorkshopReservations() + '\n' + \
             generateWorkshopAdmissions()


with open('query.sql', 'w') as f:
    f.write(totalQuery)
