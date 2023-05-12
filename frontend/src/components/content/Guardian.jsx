import React from "react";
import GuardianHeader from "./GuardianElements/GuardianHeader.jsx";
import GuardianStats from "./GuardianElements/GuardianStats";
import GuardianEquipment from "./GuardianElements/GuardianEquipment";
const Guardian = ({ guardian }) => {
	return (
		<div className='mx-auto p-3 m-5 flex flex-row w-full h-full md:max-w-[35rem]'>
			<div className='rounded-xl h-full bg-secondary w-full'>
				<GuardianHeader guardian={guardian}></GuardianHeader>
				<hr />
				<GuardianStats guardian={guardian}></GuardianStats>
				<hr />
				<GuardianEquipment guardian={guardian}></GuardianEquipment>
			</div>
		</div>
	);
};

export default Guardian;
