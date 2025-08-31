import React from 'react'

const LeaveStudent = () => {
  return (
    <div className="table-container">
      <table className="user-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Leave-Date</th>
            <th>Leave Day Count</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>687673ffcd84d0feecb18f6d</td>
            <td>
              <span>Rose Dongol</span>
            </td>
            <td>2024-01-15</td>
            <td>5 days</td>
          </tr>
          <tr>
            <td>687673ffcd84d0feecb18f6d</td>
            <td>
              <span>Prashant Shrestha</span>
            </td>
            <td>2024-01-15</td>
            <td>0 days</td>
          </tr>
          <tr className='status-red'>
            <td>687673ffcd84d0feecb18f6d</td>
            <td>
              <span>Saya Bogati</span>
            </td>
            <td>2024-01-15</td>
            <td>25 days</td>
          </tr>
        
        </tbody>
      </table>
    </div>
  )
}

export default LeaveStudent
