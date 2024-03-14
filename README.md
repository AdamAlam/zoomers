## Starting the Frontend (NextJS)

- Ensure you have the `.env.local` file in the fronted directory

### Install dependencies

```bash
npm install
```

---

### Run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

This project uses [`next/font`](https://nextjs.org/docs/basic-features/font-optimization) to automatically optimize and load Inter, a custom Google Font.

## Starting the Backend (FastAPI)

- Ensure you have the `.env` file in the backend directory

### CD into Backend Directory

```bash
cd backend
```

---

### Create virtual environment

```bash
python -m venv env
```

---

### Activate venv

MacOS/Linux:

```bash
source ./env/bin/activate
```

Windows Powershell:

```sh
.\env\Scripts\Activate.ps1
```

Windows Bash:

```bash
source ./env/Scripts/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Start the application

```bash
uvicorn main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) with your browser to see the result.
