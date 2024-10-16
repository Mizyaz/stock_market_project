// frontend/app/components/ErrorMessage.tsx

import { FC } from 'react'

interface ErrorMessageProps {
  message: string
}

const ErrorMessage: FC<ErrorMessageProps> = ({ message }) => {
  return (
    <div className="mt-4 p-4 bg-red-100 text-red-700 rounded">
      <p>{message}</p>
    </div>
  )
}

export default ErrorMessage