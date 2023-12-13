// SetTime.js
import React, { useState } from "react";
import axios from 'axios';

const SetTime = () => {
    const [wakeUpTime, setWakeUpTime] = useState('');
    const [sleepLevel, setSleepLevel] = useState('');
    const [showForm, setShowForm] = useState(false);

    const handleSetTimeToggle = () => {
        setShowForm((prevShowForm) => !prevShowForm);
    };

    const handleSetTime = async () => {
        try {
            const userId = sessionStorage.getItem('userid');
            const response = await axios.post('http://localhost:5000/set_time', {
                user_id: userId,
                WakeUpTime: wakeUpTime,
                SleepLevel: sleepLevel
            });

            // サーバーからのレスポンスを使った追加の処理をここに追加

        } catch (error) {
            console.error('セットエラー', error);
        }
    };

    return (
        <div className="w-[60%] mx-auto bg-red rounded-[20px] mt-10 px-4 py-0 bg-blue-500">
            <button onClick={handleSetTimeToggle} className="text-[16px] text-white px-2 py-1 rounded-md">時間を設定</button>
            {showForm && (
                <div className="text-[14px] mt-2">
                    <div>
                        <label htmlFor="wakeUpTime">時間を設定</label>
                        <input
                            type="time"
                            id="wakeUpTime"
                            value={wakeUpTime}
                            onChange={(e) => setWakeUpTime(e.target.value)}
                            className="border rounded-md px-2 py-1"
                        />
                    </div>
                    <div>
                        <label className="mt-2">今朝はよく眠れましたか？</label>
                        <div className="flex justify-between">
                            {[1, 2, 3, 4, 5].map((value) => (
                                <div key={value} >
                                    <input
                                        type="radio"
                                        id={`sleepLevel${value}`}
                                        name="sleepLevel"
                                        value={value.toString()}
                                        onChange={(e) => setSleepLevel(e.target.value)}
                                    />
                                    {/* <label htmlFor={`sleepLevel${value}`}>{value}</label> */}
                                </div>
                            ))}
                        </div>
                    </div>
                    <button onClick={handleSetTime} className="bg-green-500 text-white px-2 rounded-md my-2">送信</button>
                </div>
            )}
        </div>
    );
}

export default SetTime;
