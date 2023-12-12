import './App.css'
import Login from './components/Login';
import SignUp from './components/Signup'

function App() {
  return (
    <div className="text-4xl text-center">
      <header className="my-20">
        App Title
      </header>
      <div>
        <img src='/img/tree-icon.png' alt='tree-icon' className='w-[60%] mx-auto my-20'></img>
      </div>
      <Login />
      <SignUp />
    </div>
  );
}

export default App;
