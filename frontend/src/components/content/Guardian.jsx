import React from "react";
import GuardianHeader from "./GuardianElements/GuardianHeader.jsx";
import GuardianStats from "./GuardianElements/GuardianStats";
const Guardian = ({ guardian }) => {
	console.log(guardian);
	return (
		<div className='mx-auto p-3 m-5 flex flex-row w-full h-96 md:max-w-[35rem]'>
			<div className='rounded-xl h-full bg-secondary w-full'>
				<GuardianHeader guardian={guardian}></GuardianHeader>
				<hr />
				<GuardianStats guardian={guardian}></GuardianStats>
			</div>
		</div>
	);
};

export default Guardian;
