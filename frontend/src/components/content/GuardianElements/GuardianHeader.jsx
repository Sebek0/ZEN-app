import React from "react";
import ReactTimeAgo from "react-time-ago";
import { BUNGIE_URL } from "../../../const/BungieUrl";

const GuardianHeader = ({ guardian }) => {
	return (
		<div
			className='flex flex-row w-full h-[95px] rounded-t-xl justify-between items-center shadow-lg'
			style={{
				backgroundImage: `url(${BUNGIE_URL + guardian.emblemBackgroundPath})`,
				backgroundSize: "fit",
			}}>
			<div className='flex flex-col justify-start ml-20 p-4'>
				<span className='text-white text-xl font-extrabold text-bold drop-shadow-custom font-sans'>
					{guardian.char_class.toUpperCase()}
				</span>
				<span className='text-purple-500 rounded-xl font-sans font-extrabold text-bold text-lg font-shadow'>
					{guardian.title.name}
				</span>
			</div>
			<div className='flex flex-col justify-end rounded-xl'>
				<div className='flex flex-col mb-1 drop-shadow-2xl'>
					<div className='flex flex-row justify-center items-center'>
						<svg
							version='1.1'
							xmlns='http://www.w3.org/2000/svg'
							width='16'
							height='32'
							className='drop-shadow-custom'
							viewBox='0 0 32 32'>
							<path
								fill='#f5bd00'
								d='M22.962 8.863c-2.628-2.576-4.988-5.407-7.045-8.458l-0.123-0.193c-2.234 3.193-4.556 5.993-7.083 8.592l0.015-0.016c-2.645 2.742-5.496 5.245-8.542 7.499l-0.184 0.13c3.341 2.271 6.262 4.682 8.943 7.335l-0.005-0.005c2.459 2.429 4.71 5.055 6.731 7.858l0.125 0.182c4.324-6.341 9.724-11.606 15.986-15.649l0.219-0.133c-3.401-2.168-6.359-4.524-9.048-7.153l0.010 0.010zM18.761 18.998c-1.036 1.024-1.971 2.145-2.792 3.35l-0.050 0.078c-0.884-1.215-1.8-2.285-2.793-3.279l0 0c-1.090-1.075-2.28-2.055-3.552-2.923l-0.088-0.057c1.326-0.969 2.495-1.988 3.571-3.097l0.007-0.007c1.010-1.051 1.947-2.191 2.794-3.399l0.061-0.092c0.882 1.32 1.842 2.471 2.912 3.51l0.005 0.005c1.089 1.072 2.293 2.034 3.589 2.864l0.088 0.053c-1.412 0.905-2.641 1.891-3.754 2.994l0.002-0.002z'></path>
						</svg>
						<span className='text-yellow-500 text-center text-xl p-1 font-shadow font-extrabold text-bold drop-shadow-custom font-sans'>
							{guardian.light}
						</span>
					</div>
					<div className='flex flex-row drop-shadow-custom font-extrabold text-bold font-sans mx-1 '>
						<svg
							xmlns='http://www.w3.org/2000/svg'
							fill='none'
							viewBox='0 0 24 24'
							strokeWidth={1.5}
							stroke='white'
							className='w-6 h-6 m-auto font-shadow'>
							<path
								strokeLinecap='round'
								strokeLinejoin='round'
								d='M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z'
							/>
						</svg>

						<span className='text-gray-300 text-center text-xs p-1 drop-shadow-2xl text-bold font-shadow'>
							<ReactTimeAgo
								date={guardian.last_login}
								locale='en'
							/>
						</span>
					</div>
				</div>
			</div>
		</div>
	);
};

export default GuardianHeader;
