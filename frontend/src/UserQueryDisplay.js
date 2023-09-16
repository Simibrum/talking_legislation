import React from 'react';

const UserQueryDisplay = ({ titleName, output }) => {
  return (
    <div className="mt-5">
      <h2 className="mt-2">{titleName}</h2>
      <p className="lead mt-3 pl-3">{output}</p>
      <hr />
    </div>
  );
};

export default UserQueryDisplay;
