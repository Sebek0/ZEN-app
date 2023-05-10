import React from "react";
import { BUNGIE_URL } from "../../../const/BungieUrl";

const GuardianStats = ({guardian}) => {
	return (
		<div
			className='flex flex-row w-full h-3/12 rounded-t-xl p-5'>
			<img
				src={BUNGIE_URL + "/common/destiny2_content/icons/41c0024ce809085ac16f4e0777ea0ac4.png"}
				alt='Zen'
				width={75}
				height={75}
				className='ms-0 my-auto rounded-lg'></img>
			<div className='text-white text-lg w-9/12'>
                <p>{guardian.name}</p>
            </div>
		</div>
	);
}

export default GuardianStats;
