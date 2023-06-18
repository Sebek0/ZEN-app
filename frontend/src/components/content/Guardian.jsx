import React from "react";
import GuardianEquipment from "./GuardianElements/GuardianEquipment";
import GuardianHeader from "./GuardianElements/GuardianHeader.jsx";
import GuardianStats from "./GuardianElements/GuardianStats";

const Guardian = ({ guardian }) => {
	console.log(guardian);
	return (
		<div className='mx-auto p-2 m-5 flex flex-row w-full h-full md:min-w-[30.5rem] md:max-w-[30rem] appear'>
			<div className='rounded-xl h-full bg-secondary w-full flex flex-col justify-between'>
				<div>
					<GuardianHeader guardian={guardian} />
					<GuardianStats guardian={guardian} />
					<GuardianEquipment guardian={guardian} />
				</div>

				<div className='flex flex-col p-3 text-center text-xl w-auto pt-52'>
					<h1 className='text-accent'>
						Total <strike>Wasted</strike> Played Time
					</h1>
					<span className='text-white'>
						This person played {guardian.minutesPlayedTotal} minutes
						<span className='text-accent'>
							{" "}
							(or {Math.floor(guardian.minutesPlayedTotal / 60)} hours)
						</span>{" "}
						on this character
					</span>
				</div>
			</div>
		</div>
	);
};

export default Guardian;
