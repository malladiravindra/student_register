import React, { useState, useEffect } from 'react';
import './Dashboard.css';

function Dashboard({ teacher, onLogout }) {
  const [attendanceData, setAttendanceData] = useState(null);

  useEffect(() => {
    fetchAttendance();
  }, []);

  const fetchAttendance = async () => {
    try {
      const response = await fetch('/api/dashboard/', {
        method: 'GET',
        credentials: 'include',
      });
      if (response.ok) {
        const data = await response.json();
        setAttendanceData(data);
      }
    } catch (err) {
      console.error('Error fetching attendance:', err);
    }
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Welcome, {teacher.name}</h1>
        <button onClick={onLogout} className="logout-btn">Logout</button>
      </header>
      {attendanceData && (
        <div className="attendance-summary">
          <h2>Attendance for {attendanceData.date}</h2>
          <div className="stats">
            <div className="stat-card">
              <h3>Total Students</h3>
              <p className="stat-number">{attendanceData.total_students}</p>
            </div>
            <div className="stat-card present">
              <h3>Present</h3>
              <p className="stat-number">{attendanceData.present_students}</p>
            </div>
            <div className="stat-card absent">
              <h3>Absent</h3>
              <p className="stat-number">{attendanceData.absent_students}</p>
            </div>
          </div>
          <h3>Student List:</h3>
          <ul className="student-list">
            {attendanceData.students.map(student => (
              <li key={student.id} className={attendanceData.attendance_dict[student.id] ? 'present' : 'absent'}>
                {student.name} ({student.roll_number}) - {attendanceData.attendance_dict[student.id] ? 'Present' : 'Absent'}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default Dashboard;