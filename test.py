from prisma import Prisma

def main() -> None:
    db = Prisma()
    db.connect()

    print('connected to db')

    db.disconnect()

if __name__ == '__main__':
    main()