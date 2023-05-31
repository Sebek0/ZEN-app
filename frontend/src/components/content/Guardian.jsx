import React from "react";
import GuardianEquipment from "./GuardianElements/GuardianEquipment";
import GuardianHeader from "./GuardianElements/GuardianHeader.jsx";
import GuardianStats from "./GuardianElements/GuardianStats";
const Guardian = ({ guardian }) => {
	return (
		<div className='mx-auto p-2 m-5 flex flex-row w-full h-full md:min-w-[30rem] md:max-w-[30rem]'>
			<div className='rounded-xl h-full bg-secondary w-full'>
				<GuardianHeader guardian={guardian}></GuardianHeader>
				<GuardianStats guardian={guardian}></GuardianStats>
				<GuardianEquipment guardian={guardian}></GuardianEquipment>
			</div>
		</div>
	);
};

export default Guardian;
