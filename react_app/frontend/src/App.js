//App.js
import './App.css'
import Top from './components/Top'
import Login from './components/Login'
import SignUp from './components/Signup'
import Home from './components/Home'

import {BrowserRouter,Route, Routes} from 'react-router-dom'



function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Top />} />
        <Route path='/home' element={<Home />}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App;
