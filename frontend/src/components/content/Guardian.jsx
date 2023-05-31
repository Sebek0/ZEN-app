import React from "react";
import GuardianEquipment from "./GuardianElements/GuardianEquipment";
import GuardianHeader from "./GuardianElements/GuardianHeader.jsx";
import GuardianStats from "./GuardianElements/GuardianStats";
const Guardian = ({ guardian }) => {
	console.log(guardian);
	return (
		<div className='mx-auto p-2 m-5 flex flex-row w-full h-full md:min-w-[30.5rem] md:max-w-[30rem] appear'>
			<div className='rounded-xl h-full bg-secondary w-full'>
				<GuardianHeader guardian={guardian}></GuardianHeader>
				<GuardianStats guardian={guardian}></GuardianStats>
				<GuardianEquipment guardian={guardian}></GuardianEquipment>
				<div className='flex flex-col justify-center pt-52'>
					<h1 className='text-accent text-center p-3 text-xl w-auto'>
						Total <strike>Wasted</strike> Played Time
					</h1>
					<span className='text-white text-center p-3 text-xl w-auto'>
						This person played {guardian.minutesPlayedTotal} minutes
						<span className='text-accent'> (or {Math.floor(guardian.minutesPlayedTotal/60)} hours)</span> on this character

					</span>
					</div>
			</div>
		</div>
	);
};

export default Guardian;
