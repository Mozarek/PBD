class Client:
    def __init__(self, _id, name, phone, isCompany):
        self.id = _id
        self.name = name
        self.phone = phone
        self.isCompany = isCompany


class DiscountThreshold:
    def __init__(self, _id, confID, startDate, endDate, discount):
        self.id = _id
        self.confID = confID
        self.startDate = startDate
        self.endDate = endDate
        self.discount = discount


class Conference:
    def __init__(self, _id, name, price, studentDiscount, startDate, endDate):
        self.id = _id
        self.name = name
        self.price = price
        self.studentDiscount = studentDiscount
        self.startDate = startDate
        self.endDate = endDate


class ConferenceDay:
    def __init__(self, _id, confID, date , limit):
        self.id = _id
        self.confID = confID
        self.date = date
        self.limit = limit
        self.freePlaces = limit


class Workshop:
    def __init__(self, _id, dayID, name, start, end, limit, price):
        self.id = _id
        self.dayID = dayID
        self.name = name
        self.start = start
        self.end = end
        self.limit = limit
        self.price = price
        self.freePlaces = limit


class ConferenceReservation:
    def __init__(self, _id, confID, clientID, registrationDate):
        self.id = _id
        self.confID = confID
        self.clientID = clientID
        self.registrationDate = registrationDate
        self.toPay = 0


class DayReservation:
    def __init__(self, _id, dayID, reservationID, participantsNumber, studentParticipantsNumber, toPay):
        self.id = _id
        self.dayID = dayID
        self.reservationID = reservationID
        self.participantsNumber = participantsNumber
        self.studentParticipantsNumber = studentParticipantsNumber
        self.toPay = toPay


class Participant:
    def __init__(self, _id, firstName, lastName, EMailAddress):
        self.id = _id
        self.firstName = firstName
        self.lastName = lastName
        self.EMailAddress = EMailAddress


class DayAdmission:
    def __init__(self, _id, participantID, dayReservationID, isStudent):
        self.id = _id
        self.participantID = participantID
        self.dayReservationID = dayReservationID
        self.isStudent = isStudent


class WorkshopReservation:
    def __init__(self, _id, workshopID, dayReservationID, participantsNumber):
        self.id = _id
        self.workshopID = workshopID
        self.dayReservationID = dayReservationID
        self.participantsNumber = participantsNumber
        self.notEnrolled = participantsNumber


class WorkshopAdmission:
    def __init__(self, dayAdmissionID, workshopReservationID):
        self.dayAdmissionID = dayAdmissionID
        self.workshopReservationID = workshopReservationID
