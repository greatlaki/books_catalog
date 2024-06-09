import uvicorn


def main():
    uvicorn.run(
        'main.app:app',
        host='localhost',
        port=8000,
        proxy_headers=True,
        workers=1,
        reload=True,
    )
    return


if __name__ == '__main__':
    main()
