import React, {useState} from 'react'
import axios from'axios' //HTTP通信用ライブラリ

const Login = () =>{
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    const handleLogin = async () => {
        try {
            const response = await axios.post('http://localhost:5000/login',{
                email,
                password
            })
            console.log(response.data)

        } catch (error) {
            console.error('Login failed', error)
        }
    }

    return (
        <div>
            <h1>Login</h1>
            <input
                type = "email"
                placeholder='Email'
                value = {email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <input
                type = "password"
                placeholder='Password'
                value = {password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <button onClick={handleLogin}>Login</button>
        </div>
    )
}

export default Login
