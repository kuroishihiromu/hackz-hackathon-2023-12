//Signup.js
import React, { useState } from "react";
import axios from 'axios';

const SignUp = () => {
    const [showForm, setShowForm] = useState(false);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [DeviceID, setDeviceID] = useState('');
    const [Email, setEmail] = useState('');

    const handleSignUpToggle = () => {
        // ボタンをクリックするたびに表示と非表示をトグル
        setShowForm((prevShowForm) => !prevShowForm);
    };

    const handleSignUp = async () => {
        try {
            const response = await axios.post('http://localhost:5000/signup', {
                username: username,
                password: password,
                DeviceID: DeviceID,
                Email: Email
            });
            console.log('新規登録成功:', response.data);
            sessionStorage.setItem('userid', response.data.userid)

            window.location.href = '/home';
            setShowForm(true);

        } catch (error) {
            console.error('新規登録エラー', error);
        }
    };

    return (
        <div className="w-[60%] mx-auto bg-[#b8a1c5] rounded-[12px] mt-10 px-4 p-0 shadow-lg mb-20">
            <button onClick={handleSignUpToggle} className="text-white px-2 py-5 text-[18px] font-semibold tracking-widest">新規登録</button>
            {showForm && (
                <div className="text-[12px] mt-2">
                    <div>
                        <label htmlFor="newUsername">ユーザー名:</label>
                        <input 
                            type="text"
                            id="newUsername"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="border rounded-md px-2 py-1"
                        />
                    </div>
                    <div>
                        <label htmlFor="newDeviceID" className="mt-2">デバイスID:</label>
                        <input 
                            type="text"
                            id="newDeviceID"
                            value={DeviceID}
                            onChange={(e) => setDeviceID(e.target.value)}
                            className="border rounded-md px-2 py-1"
                        />
                    </div>
                    <div>
                        <label htmlFor="newEmail" className="mt-2">メールアドレス</label>
                        <input 
                            type="text"
                            id="newEmail"
                            value={Email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="border rounded-md px-2 py-1"
                        />
                    </div>
                    <div>
                        <label htmlFor="newPassword" className="mt-2">パスワード:</label>
                        <input 
                            type="password"
                            id="newPassword"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="border rounded-md px-2 py-1"
                        />
                    </div>

                    <button onClick={handleSignUp} className="bg-red-500 text-white px-2 rounded-md my-2">登録</button>
                </div>
            )}
        </div>
    );
}

export default SignUp;
