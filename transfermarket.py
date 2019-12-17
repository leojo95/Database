import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import sys
import argparse
import request

engine = create_engine('sqlite:///transfermarket.db', echo=False)
# print engine.execute("select 1").scalar()
Base = declarative_base()

# Mapping
class position(Base):

    __tablename__ = 'position'

    pid = Column('pid',Integer, primary_key=True)
    pname = Column('pname',String(10))

    def __init__(self, pid, pname):
        self.pid = pid
        self.pname = pname


Base.metadata.create_all(engine)


class scouter(Base):

    __tablename__ = 'scouter'

    sid = Column('sid',Integer, primary_key=True)
    sname = Column('sname',String(10))
    sphone = Column('sphone',String(10))
    pid = Column('pid',Integer, ForeignKey('position.pid'))
    position = relationship("position", back_populates="scouter")

    def __init__(self, sid, sname, sphone,pid):
        self.sid = sid
        self.sname = sname
        self.sphone = sphone
        self.pid = pid


position.scouter = relationship("scouter", order_by = scouter.sid, back_populates = "position")

Base.metadata.create_all(engine)


class staff(Base):

    __tablename__ = 'staff'

    stid = Column('stid', Integer, primary_key=True)
    stname = Column('stname', String(10))
    stphone = Column('stphone', String(10))
    sid = Column('sid', Integer, ForeignKey('scouter.sid'))
    scouter = relationship("scouter", back_populates="staff")

    def __init__(self, stid, stname, stphone,sid):
        self.stid = stid
        self.stname = stname
        self.stphone = stphone
        self.sid = sid


scouter.staff = relationship("staff", order_by=staff.stid, back_populates="scouter")

Base.metadata.create_all(engine)


class player(Base):

    __tablename__ = 'player'

    plid = Column('plid', Integer, primary_key=True)
    plname = Column('plname', String(10))
    plpos = Column('plpos', String(10))
    sid = Column('sid', Integer, ForeignKey('scouter.sid'))
    scouter = relationship("scouter", back_populates="player")

    def __init__(self, plid, plname, plpos,sid):
        self.plid = plid
        self.plname = plname
        self.plpos = plpos
        self.sid = sid


scouter.player = relationship("player", order_by=player.plid, back_populates="scouter")

Base.metadata.create_all(engine)


class schedule(Base):

    __tablename__ = 'schedule'

    scid = Column('scid', Integer, primary_key=True)
    plid = Column('plid', Integer, ForeignKey('player.plid'))
    date = Column('date', String(10))
    stype = Column('stype', String(10))
    stid = Column('stid', Integer, ForeignKey('staff.stid'))
    player = relationship("player", back_populates="schedule")
    staff = relationship("staff", back_populates="schedule")

    def __init__(self, scid, plid, date, stype,stid):
        self.scid = scid
        self.plid = plid
        self.date = date
        self.stype = stype
        self.stid = stid


player.schedule = relationship("schedule", order_by=schedule.scid, back_populates="player")
staff.schedule = relationship("schedule", order_by=schedule.scid, back_populates="staff")

Base.metadata.create_all(engine)

# Creating Session
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()
session.add_all([

    position(1, 'General Scouter'),
    position(2, 'Assistant Scouter'),
    position(3, 'Youth Scouter'),

    scouter(101, 'Solskjaer', '408-0290', 1),
    scouter(102, 'Giggs', '826-8596', 2),
    scouter(103, 'Scholes', '221-3253', 2),
    scouter(104, 'Neville', '419-5608', 3),
    scouter(105, 'Rooney', '339-4191', 3),
    scouter(106, 'Saha', '233-8520', 3),

    staff(201, 'BAE', ' 867-3438', 201),
    staff(202, 'LEE', '881-8899', 202),
    staff(203, 'PARK', '960-1378', 203),
    staff(204, 'KIM', '668-0256', 204),
    staff(205, 'HWANG', '776-5221', 205),
    staff(206, 'HONG', '908-1445', 206),

    player(32658, 'Ronaldo', 'FW', 1),
    player(23455, 'Messi', ' FW', 1),
    player(73956, 'Neymar', 'FW', 1),
    player(50239, 'Holland', 'FW', 1),
    player(43539, 'Mbappe', 'FW', 1),
    player(51239, 'Xavi', 'MF', 2),
    player(74569, 'Iniesta', 'MF', 2),
    player(50564, 'Busquest', 'MF', 2),
    player(59678, 'Gerrard', 'MF', 2),
    player(14239, 'Lampard', 'MF', 2),
    player(53429, 'Maddison', 'MF', 3),
    player(96574, 'Havertz', 'MF', 3),
    player(17898, 'Ballack', 'MF', 3),
    player(35856, 'Hazard', 'MF', 3),
    player(17465, 'Thiago', 'MF', 4),
    player(13459, 'Benzema', 'FW', 4),
    player(97677, 'Flacao', 'FW', 4),
    player(23645, 'Cavani', 'FW', 4),
    player(13455, 'Silva', 'DEF', 5),
    player(73565, 'Varane', 'DEF', 5),
    player(73454, 'Sule', 'DEF', 5),
    player(18564, 'Tah', 'DEF', 6),
    player(19356, 'Evans', 'DEF', 6),
    player(77778, 'Leno', 'GK', 6),
    player(55443, 'Valdes', 'GK', 6),

    schedule(1901, 32658, '3JAN20', 'T', 1),
    schedule(1902, 23455, '8JAN20', 'T', 1),
    schedule(1903, 73956, '7JAN20', 'T', 1),
    schedule(1920, 50239, '7JAN20', 'T', 1),
    schedule(1961, 43539, '10JAN20', 'T', 1),
    schedule(1904, 51239, '13JAN20', 'L', 2),
    schedule(1061, 74569, '1JAN20', 'L', 2),
    schedule(1929, 50564, '4JAN20', 'T', 2),
    schedule(1951, 59678, '9JAN20', 'L', 2),
    schedule(1907, 14239, '11JAN20', 'L', 2),
    schedule(2038, 53429, '11JAN20', 'L', 3),
    schedule(1201, 96574, '13JAN20', 'T', 3),
    schedule(2901, 17898, '2JAN20', 'T', 3),
    schedule(1872, 35856, '8JAN20', 'T', 3),
    schedule(3001, 17465, '9JAN20', 'L', 4),
    schedule(8471, 13459, '12JAN20', 'L', 4),
    schedule(2841, 97677, '14JAN20', 'T', 4),
    schedule(9201, 23645, '3JAN20', 'L', 4),
    schedule(8881, 13455, '5JAN20', 'T', 5),
    schedule(7921, 73565, '6JAN20', 'T', 5),
    schedule(7901, 73454, '10JAN20', 'L', 5),
    schedule(6901, 18564, '2JAN20', 'L', 6),
    schedule(5961, 19356, '7JAN20', 'T', 6),
    schedule(4231, 77778, '3JAN20', 'T', 6),
    schedule(1021, 55443, '14JAN20', 'T', 6)
])

# Coding Command Line
def main():
    #create parser
    parser = argparse.ArgumentParser(description='This program is written to manage the transfermarket')

    parser.add_argument('-v', '--version', action="store_true", help="show the version of the program")

    # either command available
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--search', action="store_true", help="search the player")
    group.add_argument('--list', action="store_true", help="bring up the list(has option of scouter,staff and player)")
    group.add_argument('--schedule', action="store_true", help="show the scheduled meeting on the  input date(date format: 1JAN20~14JAN20)")
    group.add_argument('--count', action="store_true", help="show the number of T(Transfer)/L(loan) meetings going on")
    group.add_argument('--register', action="store_true", help="register the player(should include plid,plpos & sid)")

    parser.add_argument('name', nargs='?', default=False, help="name of the player")
    parser.add_argument('plid', nargs='?', default=False, help="player id")
    parser.add_argument('plpos', nargs='?', default=False, help="player position")
    parser.add_argument('sid', nargs='?', default=False, help="scouter id")

    args = parser.parse_args()

    if args.version:
        print('transfermarket_1.0')
        sys.exit()

    if args.search:
        searched = (session.query(player).filter(player.plname == args.name).all())
        for row in searched:
            print (row.plname, row.plid, row.plpos, row.sid)

    if args.list and (args.name == 'scouter'):
        searched = (session.query(scouter).order_by(scouter.sid).all())
        for row in searched:
            print (row.sid, row.sname, row.sphone, row.pid)

    if args.list and (args.name == 'staff'):
        searched = (session.query(staff).order_by(staff.stid).all())
        for row in searched:
            print (row.stid, row.stname, row.stphone, row.sid)

    if args.list and (args.name == 'player'):
        searched = (session.query(player).order_by(player.sid).all())
        for row in searched:
            print (row.plname, row.plid, row.plpos, row.sid)

    if args.schedule:
        searched = (session.query(schedule).filter(schedule.date == args.name).all())
        for row in searched:
            print (row.scid, row.plid, row.stype, row.stid)

    if args.count:
        transfer = (session.query(schedule).filter(schedule.stype == 'T').count())
        loan = (session.query(schedule).filter(schedule.stype == 'L').count())
        print ('T: %s L: %s' % (transfer,loan))

    if args.register:
        new_player = player(args.plid, args.name, args.plpos, args.sid)
        session.add(new_player)
        session.commit()
        session.refresh(new_player)
        print('player registered')
    elif args.register and (row.plid is None):
        print('need additional input for registration')

if __name__ == "__main__":
    main()

