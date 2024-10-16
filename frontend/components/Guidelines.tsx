// frontend/app/components/Guidelines.tsx

import { FC } from 'react'

interface GuidelinesProps {
  content: string
}

const Guidelines: FC<GuidelinesProps> = ({ content }) => {
  return (
    <div className="mt-4 p-4 bg-gray-100 rounded">
      <h3 className="text-lg font-semibold mb-2">Guidelines</h3>
      <p>{content}</p>
    </div>
  )
}

export default Guidelines