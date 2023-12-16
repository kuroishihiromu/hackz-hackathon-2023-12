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
        <div className="w-[80%] mx-auto bg-red rounded-[12px]  px-10 py-3 bg-[#b8a1c5] text-center shadow-lg">
            <button onClick={handleSetTimeToggle} className="text-[18px] text-white px-2 py-1 font-semibold">時間を設定</button>
            {showForm && (
                <div className="text-[16px] mt-2 ">
                    <div className="my-2 border-y py-2">
                        <label htmlFor="wakeUpTime"><div className="mx-3 text-white">起きる時間</div></label>
                        <input
                            type="time"
                            id="wakeUpTime"
                            value={wakeUpTime}
                            onChange={(e) => setWakeUpTime(e.target.value)}
                            className="border rounded-md px-2 py-1"
                        />
                    </div>
                    <div>
                        <label className="mt-5 text-white block mb-2">今朝はよく眠れましたか？</label>
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
