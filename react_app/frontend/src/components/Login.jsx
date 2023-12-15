//Login.js
import React, { useState } from "react";
import axios from 'axios';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [showForm, setShowForm] = useState(false);

    const handleLoginToggle = () => {
        // ボタンをクリックするたびに表示と非表示をトグル
        setShowForm((prevShowForm) => !prevShowForm);
    };

    const handleLogin = async () => {
        try {
            const response = await axios.post('http://localhost:5000/login', {
                username: username,
                password: password,
            });
            console.log('ログイン成功:', response.data);
            sessionStorage.setItem('userid', response.data.userid)
            
            // ログイン成功時の追加の処理をここに追加

            window.location.href = '/home';

        } catch (error) {
            console.error('ログインエラー', error);
        }
    };

    return (
        <div className="w-[60%] mx-auto bg-red rounded-[12px] px-4 py-0 bg-[#b8a1c5] shadow-lg">
            <button onClick={handleLoginToggle} className="text-[18px]  text-white px-2 py-5 font-semibold tracking-widest">ログイン</button>
            {showForm && (
                <div className="text-[14px] mt-2">
                    <div>
                        <label htmlFor="username">ユーザー名:</label>
                        <input 
                            type="text"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="border rounded-md px-2 py-1"
                        />
                    </div>
                    <div>
                        <label htmlFor="password" className="mt-2">パスワード:</label>
                        <input 
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="border rounded-md px-2 py-1"
                        />
                    </div>
                    <button onClick={handleLogin} className="bg-green-500 text-white px-2 rounded-md my-2">送信</button>
                </div>
            )}
        </div>
    );
}

export default Login;
